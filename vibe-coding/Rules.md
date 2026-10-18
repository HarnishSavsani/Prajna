<!-- PERMANENT RULES – AI agents must read this before every coding session -->

# Prajna – Coding Rules & AI Guardrails

**Last Updated**: 2026-10-18
**Status**: Active – must be followed by all AI agents and contributors

> **Instruction to AI**: Read this entire file before writing or modifying any code. These rules override your default preferences. Also read `Memory.md` for current state. If a rule here conflicts with a request, stop and ask.

---

## 1. Core Philosophy
- **FalkorDB is the product, not a cache.** If the feature works without FalkorDB, it's wrong.
- **Reasoning in Cypher, language in the LLM.** Never move graph logic into Python loops.
- **Permission-safe by construction.** Filter in Cypher, before the LLM, every time.
- **Explainable always.** Every answer stores its Cypher and evidence path.
- **Clean modular design.** Strong separation between graph engine, backend service, and frontend.
- **Simplicity over cleverness.** Plain Python agent loop beats a heavy framework here.
- **Honest over impressive.** Report real numbers; never fake a demo or a metric.
- **Four-day focused sprint.** Built from scratch 15–18 Oct 2026 for FalkorDB Graph Hacks.

## 2. Technology & Dependency Rules

### 2.1 Approved Stack (do not deviate without discussion)
| Category | Approved Choice | Notes |
|---|---|---|
| Graph DB (ONLY database) | FalkorDB, image `v4.20.7` | Pinned for stable Cypher & multi-graph |
| Vectors | FalkorDB vector index | No Qdrant/Pinecone/Chroma/Milvus |
| Full-text | FalkorDB full-text index | No Elasticsearch/Vespa |
| Backend | Python 3.11+, FastAPI, SSE | Streaming agent architecture |
| Unstructured ingest | Cognee + `cognee-community-hybrid-adapter-falkor` | Pinned together |
| Structured ingest | PyGithub + parameterised Cypher | Idempotent `MERGE` |
| Agent loop | Plain Python multi-agent pipeline | Router, Retriever, Historian, Actor |
| LLM routing | LiteLLM | Dual model: fast intent + prose generation |
| Frontend | Prajna `web/` (Next.js 16, React 19) | Modern responsive UI, MIT |
| Graph viewing | FalkorDB Browser | Interactive "Why?" deep dives |

### 2.2 Libraries – Allowed
FastAPI, Pydantic, the FalkorDB Python client, Cognee + its FalkorDB adapter, LiteLLM, PyGithub, python-dotenv, httpx, and dependencies in `web/package.json`.

### 2.3 Libraries – Forbidden or Strongly Discouraged
- **Any second datastore** for answers/memory/permissions (Postgres, Qdrant, Pinecone, Chroma, Milvus, Elasticsearch, Vespa, SQLite). **Hard no.**
- New UI libraries in `web/` without approval.
- Heavy agent frameworks (CrewAI, AutoGen) — debugging cost too high for 2 days.
- ORMs over FalkorDB — write Cypher directly.
- moment.js, full lodash, jQuery.

### 2.4 When you need a new dependency
Propose it first (name, why, size, licence) and wait for explicit approval. Then add it pinned to `requirements.txt`/`package.json`. Never add a dependency silently.

## 3. Code Style & Organization

### 3.1 Naming Conventions
- **Python files/modules:** `snake_case.py`. **Functions/vars:** `snake_case`. **Classes/Pydantic models:** `PascalCase`. **Constants:** `UPPER_SNAKE`.
- **Cypher query files:** `queries/<tool_name>.cypher`; the matching MCP tool is `<tool_name>`.
- **Node labels:** `PascalCase` singular (`Person`, `Service`). **Edge types:** `UPPER_SNAKE` (`CAN_READ`, `AUTHORED`).
- **Node ids:** `"<type>:<natural-key>"` (`service:payments`).
- **Frontend:** clean Next.js/React conventions; components `PascalCase`.

### 3.2 File & Folder Rules
- Follow the folder structure in Architecture.md §13.
- One concern per file; split a file over ~300 lines.
- No barrel/index re-export files on the backend.
- Backend code goes strictly under `prajna/app/...`.
- Frontend code goes strictly under `web/src/...`.

### 3.3 Python / Language Rules
- Type-hint everything; validate all request bodies with Pydantic.
- No bare `except`; catch specific exceptions; never swallow silently.
- No raw string-concatenated Cypher — **parameterised only**.
- Keep each MCP tool a single named, readable query a human can explain (hackathon rule 12).

### 3.4 Frontend Rules (Prajna Web)
- Clean component boundaries and modular hooks.
- Real-time SSE streaming consumption and optimistic updates.
- Point `INTERNAL_URL` at the Prajna backend (`http://prajna-backend:8080`).

### 3.5 Backend / API Rules
- Route handlers thin; logic in `agents/`, `tools/`, `graph/`.
- Error response shape: `{ "detail", "error_code" }`; streaming errors as an `error` packet.
- All DB access via `graph/falkor_client.py`; tenant selected from session/persona.
- Every retrieval query uses the shared `permissions.scoped_match()` prefix.

## 4. Error Handling & Resilience
- Catch specific exceptions; log with context (tool, tenant, latency).
- User-facing messages are plain and non-leaky; internal detail goes to logs.
- If the LLM or Cognee fails, return raw graph rows rather than crashing the stream.
- Never swallow errors silently; never `except: pass`.
- Emit an `error` SSE packet on stream failures so the UI can render it.

## 5. Security Rules
- Secrets only in `.env`; provide `.env.example`; never commit `.env`.
- Validate and type every input; reject unknown tenants.
- **Enforce permissions in Cypher before the LLM** on every retrieval. No exceptions.
- Never execute LLM-authored raw Cypher; the LLM only picks named tools and supplies typed params.
- Never log secrets, tokens, or restricted node contents.
- Actions are **drafts only** — never send real email/Slack/etc.
- Only public/synthetic/own data; never ingest real personal/private data.

## 6. Testing Expectations
- `verify.py` is mandatory and must reproduce every demo number (leaks=0, grounding, graph-vs-vector, entity resolution, concurrency, latency).
- A smoke test for the streaming endpoint (one hardcoded answer rendering in the UI) is required before wiring the agent.
- Unit-test the permission prefix and the `claim_task` concurrency path.
- It is acceptable to leave UI components and non-critical paths untested during the hackathon.

## 7. Performance & Accessibility
- Print per-tool query latency; target < 50 ms typical on demo data.
- Keep the demo dataset < ~100 MB.
- Keep the reused UI's keyboard navigation and visible focus states; new components meet WCAG 2.1 AA (focus ring, labels, 44×44px targets, contrast ≥ 4.5:1).
- Do not add heavy 3D/WebGL graph visuals (they cost time and didn't win last time).

## 8. AI-Specific Guardrails (Critical Section)

### Always do
- Read `Rules.md`, `PRD.md`, `Specs.md`, and `Memory.md` before starting a task.
- Keep FalkorDB the only datastore; put vectors and full-text in FalkorDB.
- Write reasoning as parameterised Cypher / `algo.*`, exposed as named MCP tools.
- Prepend `permissions.scoped_match()` to every retrieval query.
- Store an `Answer` node with the Cypher + `USED` evidence for every response.
- Maintain clean modularity between UI and API contracts.
- Pin versions (FalkorDB `v4.20.7`; Cognee + adapter together; Python 3.11–3.13; FalkorDB port 6379).
- Use DDL index syntax (`CREATE FULLTEXT INDEX FOR (n:Label) ON (n.prop)`).
- Update `Memory.md` at the end of a working session.

### Never do
- **Never add a second datastore** (Postgres/Qdrant/Pinecone/Chroma/Milvus/Elasticsearch/Vespa/SQLite) for answers, memory, or permissions.
- **Never move ranking/path/permission logic into Python** — it must be Cypher.
- Never execute LLM-authored raw Cypher.
- Never invent node labels, edge types, or fields not in Specs.md/Architecture.md.
- Never send a real message/email; actions are drafts only.
- Never ingest real personal/private data.
- Never install packages without explicit approval.
- Never commit secrets or `.env`.
- Never silence errors with bare `except` or swallow them.
- Never create giant god files/components; maintain clear separation of concerns.
- Never use the multi-arg `db.idx.fulltext.createNodeIndex` (breaks on FalkorDB 6.0).

### When uncertain
- Ask a clarifying question citing the requirement ID (FR-xxx / US-xxx).
- Or propose 2–3 options and wait.
- Or add a clearly marked `TODO` and note it in `Memory.md`.

## 9. Documentation & Comments
- Each MCP tool query file has a top comment: purpose, caller agent, parameters, which track bullet it serves.
- Keep `QUERIES.md` (every Cypher/algorithm) in sync with `queries/`.
- Update the README "Why FalkorDB is not decoration" section when adding a feature.
- Comment non-obvious Cypher (e.g., why a traversal depth is bounded).

## 10. Git & Commit Expectations
- No code or repo commits before 15 Oct 12:01 AM IST (hackathon rule 8). Pre-event: notes/diagrams only.
- Conventional-ish messages: `feat:`, `fix:`, `docs:`, `chore:`.
- Never commit `.env`, data dumps, or secrets.
- Disclose AI assistants in `AI_USAGE.md` (hackathon rule 11).

## 11. How to Update This Rules File
Propose a change with a one-line rationale; apply only after team agreement; note the change and date at the top of `Memory.md`'s Decisions section. The "FalkorDB is the only datastore" and "permissions in Cypher before the LLM" rules are non-negotiable for this project.