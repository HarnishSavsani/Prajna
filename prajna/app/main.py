import asyncio
from contextlib import asynccontextmanager
import logging
import uuid
from typing import Any, AsyncGenerator, Dict, Optional

from fastapi import FastAPI, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from prajna.app.boot_routes import router as boot_router
from prajna.app.graph.schema import init_schema
from prajna.app.ingest.github_loader import seed_github_data
from prajna.app.ingest.synthetic_overlay import seed_synthetic_overlay
from prajna.app.agents.router import router_agent
from prajna.app.agents.retriever import retriever_agent
from prajna.app.agents.historian import historian_agent
from prajna.app.agents.actor import actor_agent
from prajna.app.streaming.packets import (
    message_start_packet,
    reasoning_start_packet,
    reasoning_delta_packet,
    reasoning_done_packet,
    custom_tool_start_packet,
    custom_tool_args_packet,
    custom_tool_delta_packet,
    message_delta_packet,
    citation_info_packet,
    message_end_packet,
    section_end_packet,
    stop_packet
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("prajna")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Lifespan: Init schemas and seed graph in FalkorDB
    logger.info("Initializing Prajna schemas on FalkorDB...")
    try:
        init_schema("kirana")
        init_schema("globex")
        seed_github_data("kirana")
        seed_synthetic_overlay("kirana")
        logger.info("Prajna FalkorDB successfully bootstrapped and seeded.")
    except Exception as e:
        logger.warning(f"Could not connect to FalkorDB on startup (will retry on queries): {e}")
    yield

app = FastAPI(title="Prajna Backend", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(boot_router)
app.include_router(boot_router, prefix="/api")

class ChatMessageRequest(BaseModel):
    message: str
    chat_session_id: Optional[str] = "session-default-1"
    parent_message_id: Optional[str] = None

async def stream_chat_flow(message: str, session_id: str, tenant: str = "kirana", user_id: str = "person:admin") -> AsyncGenerator[str, None]:
    msg_id = f"msg-{uuid.uuid4().hex[:8]}"
    yield message_start_packet(msg_id)

    # 1. Reasoning & Routing
    yield reasoning_start_packet()
    yield reasoning_delta_packet(f"Analyzing query: '{message}' against FalkorDB Org Graph...")
    tool_name, params = router_agent.route(message)
    yield reasoning_delta_packet(f"Selected graph-native MCP Tool: `{tool_name}` with parameters: {params}...")
    
    # 2. Historian Recall
    memory_context = historian_agent.recall(user_id=user_id, tenant=tenant)
    if memory_context.get("has_context"):
        yield reasoning_delta_packet(f"Recalled prior context: {memory_context.get('context_prompt')}")
    yield reasoning_done_packet()

    # 3. Tool Execution via Retriever
    yield custom_tool_start_packet(tool_name)
    yield custom_tool_args_packet(tool_name, params)
    retrieval = retriever_agent.retrieve(tool_name, params, user_id=user_id, tenant=tenant)
    yield custom_tool_delta_packet(tool_name, {
        "path": retrieval.get("path", []),
        "latency_ms": retrieval.get("latency_ms", 0.0),
        "rows_count": len(retrieval.get("raw_rows", []))
    })

    # 4. Actor Synthesis & Answer Persistence
    answer, citations = actor_agent.synthesize_and_record(
        query=message,
        tool_name=tool_name,
        retrieval=retrieval,
        session_id=session_id,
        tenant=tenant
    )

    # Stream chunks
    words = answer.split(" ")
    chunk_size = 3
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size]) + " "
        yield message_delta_packet(chunk)
        await asyncio.sleep(0.01)

    # 5. Citations & Completion Packets
    for c in citations:
        yield citation_info_packet(c["citation_number"], c["document_id"])

    yield message_end_packet()
    yield section_end_packet()
    yield stop_packet("finished")

@app.post("/chat/send-chat-message")
@app.post("/api/chat/send-chat-message")
async def send_chat_message(
    body: ChatMessageRequest,
    x_tenant: Optional[str] = Header(None, alias="X-Tenant"),
    x_user_id: Optional[str] = Header(None, alias="X-User-ID")
):
    tenant = x_tenant or "kirana"
    user_id = x_user_id or "person:admin"
    session_id = body.chat_session_id or "session-default-1"

    return StreamingResponse(
        stream_chat_flow(body.message, session_id, tenant=tenant, user_id=user_id),
        media_type="text/event-stream"
    )
