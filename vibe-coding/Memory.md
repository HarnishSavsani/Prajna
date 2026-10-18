# Prajna – Project Memory

<!-- LIVING DOCUMENT – AI must update this file after every significant change -->

## Rules for Updating This File
1. Newest information always goes to the **top** of each section.
2. Keep entries short, factual, and dated (YYYY-MM-DD).
3. Sprint duration: **2026-10-15 to 2026-10-18** (FalkorDB Graph Hacks 2026).
4. Never delete core historical facts — only push downward.
5. Update "Last Updated" timestamp and "Current Focus" on every edit.

**Last Updated**: 2026-10-18
**Current Phase**: Phase 5 COMPLETE (Ready for Video Demo & Final Submission)
**Overall Status**: All 7/7 verification checks passing with 1.14 ms latency on live FalkorDB. Admin routes, team member personas, full Next.js UI integration, and all 8 parameterised Cypher tools operational.
**Active Branch / Worktree**: main

---

## Current Focus
- **Phase 5 Code & Submission Assets Complete**:
  - Unit 1 done: Prajna brand, theme tokens (`prajna-brand.css`, `default/tailwind.config.js`), custom logo, and FalkorDB gradient footer.
  - Unit 2 done: Demo video script `demo-script.md` with strict 5-scene structure under 3:00.
  - Unit 3 done: Technical blog post draft `blog.md` for hackathon submission.
  - Unit 4 done: Final submission document `submission.md` covering all three tracks.
- **Verification**:
  - `make verify` passes 7/7 core verification checks (0 leaks, PageRank expert resolution, blast radius multi-hop, bus factor cardinality, atomic task claims, and multi-tenant isolation).

## Recent Decisions (newest first)
- **2026-10-18** Decision: **Admin Endpoints & Team Personas Finalized**:
  - Configured `Admin` (`admin@prajna.ai`) as primary administrator alongside team members: Rohan Gaikwad, Ronit Munde, Swati Gangurde, and Harnish Savsani.
  - Added full stub coverage for all Next.js admin endpoints (`/admin/cost-overrides`, `/admin/llm/custom-provider-names`, `/manage/admin/credential`, `/manage/admin/similar-credentials/*`, `/connector/oauth/details/*`, `/notifications/summary`, `/admin/billing/billing-information`, `/license`, `/federated`).
  - Streamlined Gateways to only `openrouter` and `litellm`.
- **2026-10-17** Decision: **Autonomous Verification Harness & Proof-of-Life**:
  - Built `prajna/verify.py` test suite validating end-to-end FalkorDB latency (<50ms target, achieving ~1.14ms), permission boundaries, intent accuracy, and optimistic concurrency.
  - Containerized stack under `prajna` Compose project (`prajna-backend`, `prajna-web`, `prajna-falkordb`).
- **2026-10-16** Decision: **Phase 3 Memory & Multi-Agent Coordination Complete**:
  - Implemented `episodes.py` (`SCOPE_PERSONAL`, `SCOPE_TEAM`, `SCOPE_ORG`), `facts.py` (bi-temporal timestamps `valid_from`/`valid_to`), `sessions.py`, and `historian.py`.
  - Added atomic compare-and-swap on `Task` nodes (`claim_task`) guaranteeing 0 double-claims across competing agents.
  - Multi-graph tenancy (`GRAPH.LIST`) tested across tenants `kirana` and `globex` with 0 cross-tenant leaks.
- **2026-10-16** Decision: **Phase 2 MCP Tool Suite & Entity Resolution**:
  - Implemented 8 parameterised Cypher tools: `who_knows`, `project_status`, `blast_radius`, `bus_factor`, `impact_ranking`, `decision_trace`, `draft_close_the_loop`, and `claim_task`.
  - Built Router agent intent classification and entity resolution without external brittle LLM calls for sub-millisecond dispatch.
- **2026-10-15** Decision: **Phase 1 Graph Ingestion & Real-Time SSE Stream**:
  - Connected `github_loader.py` and `synthetic_overlay.py` into FalkorDB with idempotent `MERGE` statements.
  - Implemented SSE streaming protocol in `prajna/app/streaming/packets.py` emitting `message_start`, `reasoning_*`, `custom_tool_*`, `message_delta`, `citation_info`, and `stop`.
- **2026-10-15** Decision: **Phase 0 Foundation & Architecture Kickoff**:
  - Hackathon kickoff: Selected FalkorDB v4.20.7 as the sole datastore (property graph, vectors, full-text).
  - Designed C4 models, openCypher schemas, and pre-LLM permission scoping invariants (`permissions.scoped_match()`).

## Progress by Phase
### Phase 0 – Foundation & Spikes (15 Oct 2026)
- [x] Repo + `docker-compose.prajna.yml` (FalkorDB v4.20.7 + backend + web)
- [x] Backend boot endpoints (`/health`, `/auth/type=disabled`, `/me`, `/settings`, `/persona`, `/llm/provider`)
- [x] `/chat/send-chat-message` structured SSE packet sequence implemented
- [x] Next.js frontend integrated and streaming verified
- [x] FalkorDB DDL schemas and full-text indexes initialized
- [x] LiteLLM dual-model configuration (`gpt-4o-mini` + `gpt-4o`)

### Phase 1 – Graph + First Flow (15 Oct 2026)
- [x] GitHub loader + synthetic org overlay + identity stitching
- [x] `permissions.scoped_match()` pre-LLM security filter
- [x] `who_knows` tool (centrality over contributions)
- [x] Live SSE streaming with "Why?" graph explanation path

### Phase 2 – All Intents + Algorithms (16 Oct 2026)
- [x] `project_status` MCP tool
- [x] `blast_radius` MCP tool (multi-hop `*1..4` dependency expansion)
- [x] `bus_factor` MCP tool (module contributor cardinality)
- [x] `impact_ranking` MCP tool (complaining customer escalation ranking)
- [x] `decision_trace` MCP tool (ADR superseding chain)
- [x] `draft_close_the_loop` customer notification action tool

### Phase 3 – Memory, Tenancy, Coordination (16 Oct 2026)
- [x] Tri-scoped episodic memory (`SCOPE_PERSONAL`, `SCOPE_TEAM`, `SCOPE_ORG`)
- [x] Temporal fact evolution (`valid_from`, `valid_to`)
- [x] Multi-graph tenant isolation (`GRAPH.LIST`)
- [x] Optimistic concurrency control on `Task` nodes (0 double-claims)

### Phase 4 – Proof + Deploy (17 Oct 2026)
- [x] `verify.py` autonomous proof-of-life harness (7/7 checks passed)
- [x] Single-command Docker Compose stack
- [x] Complete documentation: README, QUERIES.md, AI_USAGE.md

### Phase 5 – Polish + Submit (18 Oct 2026)
- [x] Demo video script prepared (`demo-script.md`)
- [x] Technical blog post prepared (`blog.md`)
- [x] Submission writeup complete (`submission.md`)
- [x] Final branding & admin interface polish

---

## Technical Invariants
- **FalkorDB is the ONLY datastore:** No Postgres, Qdrant, Pinecone, Chroma, or SQLite.
- **Permissions in Cypher:** Filtered before the LLM via `scoped_match()`.
- **Explainability:** Every response stores an `Answer` node with `USED` edges to evidence.
- **Atomicity:** `Task.version` guards concurrent claims.