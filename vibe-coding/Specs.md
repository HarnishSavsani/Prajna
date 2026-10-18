<!-- Generated with detailed vibe-coding Specs prompt. Keep in sync with PRD and Architecture. -->

# Prajna – Detailed Product Specifications

**Last Updated**: 2026-10-18
**Version**: 1.0
**Status**: Complete
**Related Documents**: PRD.md, Architecture.md, Rules.md

---

## 1. Introduction & Scope
This document specifies, at implementation level, the Prajna hackathon build. It covers ingestion, the graph model, retrieval/reasoning, permissions, memory, multi-agent coordination, the chat streaming contract to the Next.js UI, actions, and verification. Out of scope for this version: real-time sync, SSO/SCIM/billing/analytics, voice/desktop/mobile, deep research/code-sandbox/image-gen, sending real messages, and ingesting real private data. This document expands the PRD's functional requirements (FR-xxx) and the Architecture's components into concrete contracts.

## 2. Definitions, Glossary & Conventions
| Term / Abbreviation | Definition |
|---|---|
| Tenant | One organisation; one isolated FalkorDB graph key (`tenant_<slug>`) |
| Part | Product unit: customer-facing (Product/Capability/Feature) or dev-facing (Service/Module/File) |
| Identity stitching | Merging a person's tool accounts into one `Person` node |
| Permission edge | `CAN_READ` from User/Team to a Source/Doc/Service |
| MCP tool | A named, parameterised Cypher/algorithm query exposed to the agent |
| Packet | One SSE event `{placement, obj}` consumed by the reused UI |
| Episode/Fact | Memory nodes (episodic interaction / semantic statement with validity) |

**Conventions**
- Node ids: string, `<type>:<natural-key>` (e.g., `service:payments`, `person:gh_riya`). Tenant graph scopes uniqueness.
- Status values: Issue `{open, closed}`; Ticket `{new, triaged, resolved}`; Task `{open, claimed, done}`.
- Timestamps: ISO-8601 UTC strings; `valid_from`/`valid_to` on `Fact`; `valid_to = null` means current.
- All Cypher is parameterised (`$param`); no string concatenation.
- Cypher writes use `MERGE` for idempotency; `CREATE` only for append-only nodes (`Answer`, `Episode`).

## 3. Global Rules & Shared Behaviors
- **Authentication & session (demo):** `GET /auth/type` → `{"auth_type":"disabled"}`. `GET /me` → the currently selected demo persona. A UI persona switcher sets a cookie/header the backend reads to choose the current `User`. Sessions persist in FalkorDB (`Session`/`Turn`).
- **Authorization / permission model:** Every retrieval begins at the current `User` and traverses only nodes reachable via `(User)-[:CAN_READ]->` or `(User)-[:MEMBER_OF]->(:Team)-[:CAN_READ]->`. A shared Cypher prefix (`permissions.py::scoped_match`) is prepended to every tool query. Filtering happens in Cypher before any LLM call. No restricted node may appear in the answer, the citations, or the context sent to the LLM.
- **Validation philosophy:** Validate all request bodies with Pydantic; reject unknown tenants; clamp list sizes; never execute LLM-authored raw Cypher — the agent may only choose among named tools and supply typed parameters.
- **Error response format (APIs):** JSON `{ "detail": "<human message>", "error_code": "<SNAKE_CASE>" }` with appropriate HTTP status. Streaming errors are emitted as an `error` packet, not a broken stream.
- **Pagination/filtering/sorting:** List endpoints accept `limit` (default 25, max 100) and `cursor`; graph rankings return top-N with `LIMIT $n`.
- **Soft vs hard delete:** No deletes in the demo; `Fact` currency is handled by setting `valid_to`, not deleting.
- **Timestamps/timezone:** UTC everywhere; display formatting is the UI's job.
- **Audit logging:** Log chosen tool, executed Cypher (parameterised form), latency, and tenant per request. Never log secrets or restricted node contents.

## 4. Feature Specifications

### 4.1 Structured Ingestion (GitHub + synthetic overlay)
**Priority**: P0 · **PRD Reference**: US-001..003, FR-001, FR-003..005, FR-007 · **Owner Module**: `backend/app/ingest`

#### 4.1.1 Description
Load GitHub issues, PRs, reviews, releases, files, and authors for configured repos, plus a synthetic org overlay (teams, ownership, roles, permissions, private docs), into the tenant's FalkorDB graph, idempotently, with identity stitching.

#### 4.1.2 User Flows
1. Admin runs `python -m app.ingest.run --tenant kirana --repo <owner/name>`.
2. Loader pulls GitHub objects, writes nodes/edges with `MERGE`.
3. Synthetic overlay loader adds teams/ownership/permissions/private docs.
4. Identity stitching merges duplicate persons.
5. Index creation runs (idempotent).

#### 4.1.3 Detailed Functional Behavior
- Create nodes: `Person, Team, Product, Capability, Feature, Service, Module, File, Issue, PR, Release, Ticket, Doc, Decision, Source`.
- Create edges per GRAPH_MODEL (section 5.2).
- Identity stitching: match by verified email; else by exact handle/display-name; unmatched handles recorded as `Person.aliases[]` for review.
- `valid_to` set on changed facts during re-sync (FR-006).
- Idempotent: re-running changes counts by 0.

#### 4.1.4 Data & API Contracts
- CLI, not HTTP. Inputs: tenant slug, repo list, overlay file path.
- Writes only; uses `graph/falkor_client.py`.
- Emits a summary JSON `{nodes_by_label, edges_by_type, persons_merged}`.

#### 4.1.5 Acceptance Criteria
- Given a configured repo, When ingestion runs, Then node/edge counts are logged and non-zero for Issue/PR/Person/File.
- Given ingestion runs twice, Then counts do not increase on the second run.
- Given a person who is both a GitHub author and a Slack user, Then exactly one `Person` node exists.

#### 4.1.6 Edge Cases & Error Handling
- GitHub rate limit → back off and resume; partial data is acceptable; log a warning.
- Missing email → fall back to handle match; never merge two different real people on a weak match (log ambiguous pairs instead).

#### 4.1.7 UI / UX Requirements
- N/A (CLI). Admin screen is P2.

#### 4.1.8 Non-Functional Notes
- Demo dataset ingests in < 10 minutes; dataset < ~100 MB.

---

### 4.2 Unstructured Ingestion via Cognee
**Priority**: P0 · **PRD Reference**: FR-002, FR-006 · **Owner Module**: `backend/app/ingest/cognee_ingest.py`

#### 4.2.1 Description
Turn docs/discussions/markdown into `Chunk` nodes (with embeddings) and `MENTIONS` edges inside FalkorDB using Cognee's FalkorDB hybrid adapter, routed per tenant.

#### 4.2.2 User Flows
1. Admin points ingestion at a doc set.
2. Cognee `add` then `cognify` runs; graph + vectors land in FalkorDB.
3. Optional `memify` enriches entities.

#### 4.2.3 Detailed Functional Behavior
- Register the FalkorDB adapter (provider name `"falkor"`) **before** config.
- Route graph+vector handlers to FalkorDB per tenant dataset.
- Produce `Chunk{text, embedding}` and `(:Chunk)-[:MENTIONS]->(:Feature|:Service|:Person|:Decision)`.

#### 4.2.4 Data & API Contracts
- CLI/worker; config via `.env` (model, embedding model, FalkorDB host/port 6379).
- Output: chunk count, mention-edge count.

#### 4.2.5 Acceptance Criteria
- Given a doc, When cognify runs, Then its chunks are vector-queryable in FalkorDB and linked by `MENTIONS`.
- Given two tenants, Then their Cognee datasets map to different FalkorDB graphs.

#### 4.2.6 Edge Cases & Error Handling
- Cognee failure → ingestion logs error and continues with structured data; retrieval still works on structured graph.
- Port mismatch (known bug) → enforce FalkorDB on 6379.

#### 4.2.7 UI / UX Requirements
- N/A.

#### 4.2.8 Non-Functional Notes
- Run once on a curated doc set; cache results to control cost.

---

### 4.3 Permission-Filtered Retrieval
**Priority**: P0 (flagship) · **PRD Reference**: US-005, FR-009 · **Owner Module**: `backend/app/graph/permissions.py`

#### 4.3.1 Description
A single, reusable Cypher prefix that scopes every retrieval to what the current user may read, enforced before any LLM call.

#### 4.3.2 User Flows
Happy path: authorised user asks → full answer. Restricted path: unauthorised user asks → "no access" response; no restricted node in output.

#### 4.3.3 Detailed Functional Behavior
- `scoped_match(user_id)` returns a Cypher fragment binding `allowed` sources/docs/services for that user (direct and via team).
- Every tool query starts from `allowed` and never matches nodes outside it.
- The restricted response is deterministic text + mascot "restricted" state; it does not reveal the existence of specific restricted titles.

#### 4.3.4 Data & API Contracts
- Internal function, not an endpoint. Input: `user_id`, `tenant`. Output: Cypher fragment + params.

#### 4.3.5 Acceptance Criteria
- Given a doc readable only by Security, When an intern asks about it, Then the answer is "no access" and no restricted node appears in evidence/citations.
- Given the leak test (N × roles), Then leaks = 0.
- Given logs, Then the context passed to the LLM contains no restricted node.

#### 4.3.6 Edge Cases & Error Handling
- User with no permissions → empty allowed set → "no accessible data" response.
- Node reachable by two paths (one allowed) → visible (reachable via allowed path).

#### 4.3.7 UI / UX Requirements
- Restricted state: clear message; mascot eye closes (Design.md).

#### 4.3.8 Non-Functional Notes
- Prefix adds negligible latency (indexed lookups).

---

### 4.4 Conversational Q&A + MCP Tools
**Priority**: P0 · **PRD Reference**: US-001..003, 010, 011, FR-008, FR-010..012 · **Owner Module**: `backend/app/agents`, `backend/app/tools`

#### 4.4.1 Description
A multi-agent loop (Router → Retriever → Historian → Actor) answers five intents by selecting named MCP tools (each one Cypher/algorithm), permission-filtered, with entity resolution.

#### 4.4.2 User Flows
Mermaid sequence in Architecture §7. Router picks a tool; Retriever runs it; Actor writes the `Answer`.

#### 4.4.3 Detailed Functional Behavior — intents → tools
| Intent | Tool | Core query |
|---|---|---|
| who-knows | `who_knows(service)` | PageRank over AUTHORED/REVIEWED in service modules |
| dependency/blast | `blast_radius(service)` | multi-hop CALLS/DEPENDS_ON + betweenness ranking |
| status | `project_status(feature)` | issues+PRs+releases+linked messages |
| impact ranking | `impact_ranking()` | distinct complaining customers per feature |
| why/decision | `decision_trace(id)` | Decision→BASED_ON/SUPERSEDES→sources |
| bus factor | `bus_factor(module)` | distinct recent contributors per module |
| semantic lookup | `search_chunks(query)` | FalkorDB vector query + graph expansion |
| coordination | `claim_task(id, version)` | optimistic claim |

- Entity resolution (FR-012): resolve a mentioned name to a node via full-text/alias; LLM disambiguates only on ties.
- The LLM selects a tool and supplies typed params; it never writes raw Cypher.

#### 4.4.4 Data & API Contracts
- Each tool: typed input (Pydantic) → rows + a `path` structure (for "Why?").
- Tool registry exposed via MCP; also callable in-process.

#### 4.4.5 Acceptance Criteria
- Given each intent's golden questions, Then the correct tool is chosen and a correct, permission-filtered answer with a path is returned.
- Given an ambiguous name with a matching node, Then the entity resolves to that node.

#### 4.4.6 Edge Cases & Error Handling
- No tool matches → fall back to `search_chunks` + a hedged answer.
- Empty result → say so plainly; do not hallucinate.

#### 4.4.7 UI / UX Requirements
- Tool step rendered via `custom_tool_*` packets; path in "Why?".

#### 4.4.8 Non-Functional Notes
- Per-tool latency printed; < 50 ms typical on demo data.

---

### 4.5 "Why?" Trace & Citations
**Priority**: P0 · **PRD Reference**: US-004, FR-013, FR-023 · **Owner Module**: `backend/app/agents/actor.py`, `streaming`

#### 4.5.1–4.5.3
Every answer creates an append-only `Answer{question, cypher, created_at}` with `USED` edges to evidence nodes. The "Why?" view shows reasoning steps (reasoning packets), the graph path (custom-tool data), and clickable citations (citation packets map to source URLs/node ids).

#### 4.5.4 Data & API Contracts
- `Answer` node + `USED` edges. Citations stream as `citation_info{citation_number, document_id}`.

#### 4.5.5 Acceptance Criteria
- Given any answer, When "Why?" is opened, Then path + ≥1 working source link are shown, matching the stored Cypher.

#### 4.5.6–4.5.8
Missing source URL → show node id instead. Empty state if no evidence (should not happen for grounded answers). Must not expose restricted nodes.

---

### 4.6 Memory (personal/team/org, time-valid)
**Priority**: P0 · **PRD Reference**: US-006, FR-014..016 · **Owner Module**: `backend/app/memory`

#### 4.6.1–4.6.3
Store `Episode` (episodic), `Fact` (semantic, with `valid_from/valid_to`), and reusable procedures (procedural). Scope edges: `SCOPE_PERSONAL→Person`, `SCOPE_TEAM→Team`, `SCOPE_ORG→Tenant`. "Continue where we left off" recalls the user's recent episodes. Current facts (`valid_to IS NULL`) are preferred.

#### 4.6.4 Data & API Contracts
- Written by Historian/Actor; read by Historian. No separate store.

#### 4.6.5 Acceptance Criteria
- Given a prior session's personal memory, When the user returns, Then recommendations build on it.
- Given an outdated fact, Then it is shown as superseded, not as current.

#### 4.6.6–4.6.8
Conflicting facts → newest current wins; keep history via `valid_to`. No cross-user leakage (personal scope is user-filtered).

---

### 4.7 Multi-Agent Coordination & Concurrency
**Priority**: P0 · **PRD Reference**: US-008, FR-017 · **Owner Module**: `backend/app/agents`, `tools/claim_task`

#### 4.7.1–4.7.3
Agents hand off via `Task{status, version}` nodes and `HANDED_OFF` edges. A claim updates only if `status='open' AND version=$v`, incrementing version. Exactly one of two concurrent claims wins.

#### 4.7.5 Acceptance Criteria
- Given two agents claiming the same open task concurrently, Then one succeeds and the other gets no rows and picks another task; 0 double-claims in the concurrency test.

#### 4.7.6
Lost claim → retry on next open task; stale version → re-read and retry.

---

### 4.8 Multi-Tenancy
**Priority**: P0 · **PRD Reference**: US-007, FR-018 · **Owner Module**: `backend/app/config.py`, `graph`

#### 4.8.1–4.8.3
Each tenant is a separate FalkorDB graph key. The backend resolves tenant from the persona/session and selects that graph for all queries. Cognee datasets route per tenant.

#### 4.8.5 Acceptance Criteria
- Given tenants A and B, When a query runs in A, Then no B node is returned; `GRAPH.LIST` shows both.

---

### 4.9 Actions (drafts only)
**Priority**: P1 · **PRD Reference**: US-009, FR-019..021 · **Owner Module**: `backend/app/agents/actor.py`

#### 4.9.1–4.9.3
Draft a close-the-loop notification to everyone affected by a shipped fix (recipients computed from Ticket→Issue→PR→Release graph paths), or draft an issue/ticket from a question. Nothing is sent.

#### 4.9.5 Acceptance Criteria
- Given a shipped fix, When the user requests notifications, Then the draft lists exactly the graph-derived affected customers and the release link; no message is sent.

---

### 4.10 Chat UI + Real-Time Streaming Contract
**Priority**: P0 · **PRD Reference**: US-004, FR-022, FR-025 · **Owner Module**: `prajna/app/streaming`, `web/`

#### 4.10.1 Description
Serve the Next.js web application and implement the backend endpoints and SSE packet stream, so the UI renders Prajna answers, tool steps, reasoning deltas, and citations in real time.

#### 4.10.2 Boot endpoints (minimum)
| Endpoint | Method | Response (minimum) |
|---|---|---|
| `/health` | GET | `{"status":"ok"}` |
| `/auth/type` | GET | `{"auth_type":"disabled"}` |
| `/me` | GET | current persona `User` |
| `/settings` | GET | minimal settings object |
| `/enterprise-settings` | GET | Prajna branding or 404 |
| `/persona`, `/persona/labels` | GET | one "Prajna" persona |
| `/llm/provider` | GET | configured providers/models |
| `/chat/create-chat-session` | POST | `{chat_session_id}` |
| `/chat/get-user-chat-sessions` | GET | session list |
| `/chat/get-chat-session/{id}` | GET | messages |
| `/chat/send-chat-message` | POST | **SSE packet stream** (below) |
| `/chat/rename-chat-session`, `/chat/delete-chat-session/{id}` | PUT/DELETE | optional |

#### 4.10.3 `send-chat-message` request (from UI)
```json
{ "message": "string", "chat_session_id": "string", "parent_message_id": null,
  "file_descriptors": [], "internal_search_filters": null, "deep_research": false,
  "allowed_tool_ids": [], "forced_tool_id": null, "llm_override": null,
  "llm_overrides": null, "origin": "webapp", "additional_context": null }
```

#### 4.10.4 `send-chat-message` response — SSE packets
Each event: `{ "placement": {"turn_index": int, "tab_index"?: int, "sub_turn_index"?: int|null}, "obj": { ... } }`. Minimum sequence:
1. `{"type":"message_start","id":"<msgId>","content":""}`
2. `{"type":"reasoning_start"}`, then `{"type":"reasoning_delta","reasoning":"..."}` (the thinking / graph steps), then `{"type":"reasoning_done"}`
3. `{"type":"custom_tool_start","tool_name":"who_knows"}`, `{"type":"custom_tool_args","tool_name":"who_knows","tool_args":{...}}`, `{"type":"custom_tool_delta","tool_name":"who_knows","response_type":"json","data":{"path":[...]}}`
4. `{"type":"message_delta","content":"..."}` × N (answer text with inline citation markers like `[1]`)
5. `{"type":"citation_info","citation_number":1,"document_id":"<id-or-url>"}`
6. `{"type":"message_end"}`, `{"type":"section_end"}`, `{"type":"stop","stop_reason":"finished"}`

Heartbeats (`chat_heartbeat`) may be sent during quiet phases; the UI drops them.

#### 4.10.5 Acceptance Criteria
- Given the unmodified UI, When a user sends a message, Then streamed text, one tool step, reasoning, and ≥1 clickable citation render correctly.
- Given a restricted question, Then the stream yields the "no access" answer with no restricted citation.

#### 4.10.6 Edge Cases
- LLM error → emit `error` packet, not a broken stream.
- Rate limit → emit `error` with `error_code` the UI recognises.

#### 4.10.7 UI / UX Requirements
- Rebrand (name/logo/colors/favicon); remove `ee`; hide unused features (deep research, code, voice, admin connectors).

#### 4.10.8 Non-Functional Notes
- First token < 2 s typical.

---

### 4.11 Verification Harness
**Priority**: P0 · **PRD Reference**: FR-024 · **Owner Module**: `backend/verify.py`

#### 4.11.1–4.11.5
`verify.py` runs the golden set and outputs JSON + console table for: permission leaks (0), grounding %, graph-vs-vector scores, entity-resolution %, optional duplicate Hit@3, concurrency (0 double-claims), and latency. Acceptance: running `python verify.py` reproduces every number used in the demo video.

## 5. Data Model Details

### 5.1 Node fields
| Node | Fields (type) | Constraints |
|---|---|---|
| Tenant | id(str), name(str) | id unique |
| Person | id(str), display_name(str), emails(list), handles(map), aliases(list) | id unique; stitched |
| Team | id, name | |
| Product/Capability/Feature | id, name | hierarchy via PART_OF |
| Service/Module/File | id, name, path | |
| Issue | id, title, state, created_at, closed_at | state ∈ {open,closed} |
| PR | id(number), title, merged_at | |
| Release | id(tag), released_at | |
| Ticket | id, title, status, created_at | status ∈ {new,triaged,resolved} |
| Doc | id, title, url, updated_at | |
| Message | id, channel, ts, text | |
| Decision | id, text, decided_at, source_url | |
| Chunk | text, embedding(vector) | vector-indexed |
| Fact | text, valid_from, valid_to, confidence | valid_to null = current |
| Source | id, type, name | |
| Session/Turn | id, user_id, started_at | |
| Answer | question, cypher, created_at | append-only |
| Agent | name, role | |
| Task | id, status, version(int) | optimistic concurrency |
| Episode | ts, summary, scope | scope ∈ {personal,team,org} |

### 5.2 Relationships (cardinality)
`Person 1-* PR (AUTHORED), *-* PR (REVIEWED), 1-* Issue (REPORTED)`; `Person *-1 Team (MEMBER_OF)`; `Team 1-* Service/Feature (OWNS)`; `PR *-* File (TOUCHES)`; `File *-1 Module *-1 Service (PART_OF)`; `Service 1-* Feature (SERVES)`; `Feature *-1 Capability *-1 Product (PART_OF)`; `Service *-* Service (CALLS/DEPENDS_ON)`; `Ticket *-1 Feature (ABOUT)`; `Ticket *-1 Issue (ESCALATED_TO)`; `PR *-* Issue (FIXES)`; `Issue *-1 Issue (DUPLICATE_OF)`; `Release 1-* PR (CONTAINS)`; `Decision *-* (BASED_ON), *-1 Decision (SUPERSEDES)`; `Chunk *-* (MENTIONS)`; `(User|Team) *-* Source/Doc/Service (CAN_READ)`; `Session 1-* Turn; Turn 1-1 Answer (PRODUCED); Answer *-* evidence (USED)`; `Agent *-* Task (CLAIMED), Agent *-* Agent (HANDED_OFF)`.

### 5.3 Indexes
- `CREATE INDEX FOR (p:Person) ON (p.id)` (and Service, Feature, Issue, PR).
- `CREATE FULLTEXT INDEX FOR (d:Doc) ON (d.text)`; same for `Message`.
- `CREATE VECTOR INDEX FOR (c:Chunk) ON (c.embedding) OPTIONS {dimension: <d>, similarityFunction:'cosine'}`.

### 5.4 Denormalisation
- `Person.handles` map stored for fast cross-tool lookup.
- Optional cached `Service.tier` for ranking display.

## 6. Cross-Cutting Technical Specifications
- **API style:** REST + SSE; JSON bodies; snake_case fields to match the reused UI.
- **Auth token handling:** demo "disabled"; persona via cookie/header; no tokens stored.
- **File upload:** out of scope for the demo (UI control hidden).
- **Background jobs:** ingestion is CLI/worker, not a live queue.
- **Notification templates:** draft text templates for close-the-loop and issue drafts; rendered, never sent.

## 7. Out of Scope (Reinforced)
Real-time sync; SSO/SCIM/billing/analytics; voice/desktop/mobile; deep research/code-sandbox/image-gen; sending real messages; ingesting real private data; a second datastore of any kind; LLM-authored raw Cypher execution.

## 8. Open Specifications & TBD Items
1. Exact embedding dimension (depends on chosen embedding model).
2. Final list of demo repos and synthetic overlay contents.
3. Whether to render an in-app graph path view or link to FalkorDB Browser for "Why?" (P1).
4. Exact `algo.*` signatures on the pinned FalkorDB version (verify Day 1).
5. Whether Slack/Jira/Confluence are live or synthetic.