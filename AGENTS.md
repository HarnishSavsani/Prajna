# PRAJNA PROJECT KNOWLEDGE BASE & AI HARNESS

Welcome to **Prajna (प्रज्ञा)** — the graph-native Organizational Intelligence Engine built natively on top of FalkorDB with a modern Next.js/React interface. Built from scratch between **October 15 to October 18, 2026** for the FalkorDB Graph Hacks 2026 Hackathon.

## CRITICAL PROJECT DIRECTIVES (AI MUST READ BEFORE CODING)

Before writing or modifying any code in this repository, you **MUST** read the following documents in `vibe-coding/`:

1. **`vibe-coding/Rules.md`** — Core philosophy, technology constraints, and AI guardrails.
2. **`vibe-coding/Memory.md`** — Current state, sprint history (15–18 Oct 2026), and active focus.
3. **`vibe-coding/Architecture.md`** — C4 models, FalkorDB schema, service boundaries, and request flow.
4. **`vibe-coding/Specs.md`** — Feature specifications, API boot contracts, and SSE packet formats.
5. **`vibe-coding/Phases.md`** — Living implementation plan and Phase 0-5 vertical slice checklist.
6. **`vibe-coding/PRD.md`** — User stories and hackathon acceptance criteria.
7. **`vibe-coding/Design.md`** — UI design specifications, theme tokens, and visual system.

---

## REPOSITORY ARCHITECTURE

```
prajna/
├── web/                        ← Prajna Frontend (Next.js 16, React 19, Tailwind CSS).
├── vibe-coding/                ← Source-of-truth project specification documents.
│
├── prajna/                     ← Prajna Backend & Graph Engine.
│   ├── app/
│   │   ├── main.py             ← FastAPI entry point & SSE streaming endpoint
│   │   ├── boot_routes.py      ← UI boot routes (/me, /settings, /admin/llm, etc.)
│   │   ├── streaming/          ← SSE packet encoders (packets.py)
│   │   ├── graph/              ← FalkorDB client, Cypher DDL schema & permission scoping
│   │   ├── agents/             ← Router, Retriever, Historian, Actor loops
│   │   ├── tools/              ← MCP tools & Cypher queries
│   │   ├── ingest/             ← GitHub loader, Cognee adapter, synthetic overlays
│   │   ├── memory/             ← Episodic, factual, and session memory
│   │   └── config.py           ← Settings & configuration
│   ├── verify.py               ← Autonomous proof-of-life and verification test harness
│   ├── requirements.txt        ← Pinned Python dependencies
│   └── Dockerfile              ← Backend container definition
│
├── docker-compose.prajna.yml    ← Compose file: FalkorDB (v4.20.7) + Prajna Backend + Web
├── AGENTS.md                    ← This harness entry point
├── Makefile                     ← Build, run, and test targets
└── .env.example                 ← Environment template
```

---

## CORE TECHNICAL RULES

- **FalkorDB is the ONLY database:** Pinned to `falkordb/falkordb:v4.20.7`. No Postgres, Qdrant, Pinecone, or SQLite.
- **Frontend & Backend Separation:** All Prajna backend services live strictly inside `prajna/`, and the frontend lives inside `web/`.
- **SSE Streaming Contract:** The chat stream at `/chat/send-chat-message` strictly follows the packet protocol in `vibe-coding/Specs.md` §4.10.
- **Cypher-First Reasoning:** Parameterised Cypher only. All queries enforce permissions before the LLM via `permissions.scoped_match()`.
- **Sprint Dates:** Developed October 15–18, 2026 for FalkorDB Graph Hacks 2026.
