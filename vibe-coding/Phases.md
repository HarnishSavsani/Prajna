<!-- Living implementation plan. Update status and checkboxes as work progresses. -->

# Prajna – Implementation Phases

**Last Updated**: 2026-10-18
**Status**: All Phases Complete (Phases 0–5 ✅)
**Related Documents**: PRD.md, Architecture.md, Specs.md, Memory.md

---

## 1. Phasing Strategy
Phases are **vertical slices** that each end in something demoable, because the hackathon is judged on a working demo, not layers. The highest risks are de-risked first: on Day 1 (15 Oct) we prove (a) the Prajna Next.js UI renders an answer from our backend via the SSE contract, and (b) FalkorDB + Cognee work on the pinned version. We then add one demo flow end-to-end before widening. The build is executed across **four focused days** (15–18 Oct 2026) culminating in proof, deploy, video, and submission. Progress is tracked with the checkboxes here, mirrored into `Memory.md`.

## 2. Phase Overview Table
| Phase | Name | Goal | Estimated Effort | Key Deliverable | Exit Criteria (summary) |
|---|---|---|---|---|---|
| 0 | Foundation & spikes | De-risk UI contract + FalkorDB/Cognee | Day 1 (15 Oct) | UI renders a streamed answer from backend | Streaming smoke test passes; FalkorDB version chosen |
| 1 | Graph + first flow | Load graph; "who-knows" end-to-end | Day 1 (15 Oct) | Who-knows answer with path | One real answer with a "Why?" path, permission-filtered |
| 2 | All intents + algorithms | 5 intents as MCP tools | Day 2 (16 Oct) | Status, blast, impact, decision, bus-factor | All 5 demo flows return correct answers |
| 3 | Memory, tenancy, coordination | Track 02 features | Day 2 (16 Oct) | Memory recall, tenant switch, concurrency | "Continue yesterday"; 0 double-claims; tenant isolation |
| 4 | Proof + deploy | Verify + ship | Day 3 (17 Oct) | `verify.py`, live URL, README | All metrics reproduced; deployed; README complete |
| 5 | Polish + submit | Video, blog, submit | Day 4 (18 Oct) | Demo video + submission | Submitted before deadline (target 8 PM IST 18 Oct) |

## 3. Detailed Phase Breakdown

### Phase 0 – Foundation & Spikes
**Goal**: Remove the two biggest unknowns before building features.
**Estimated Effort**: Day 1 morning (15 Oct).
**Dependencies**: None (hackathon has started; repo created after 15 Oct 12:01 AM IST).

**Scope – What will be done**:
- Create repo; add `docker-compose.prajna.yml` with FalkorDB pinned `v4.20.7` (+ Browser), backend, web.
- Backend skeleton (FastAPI) with `/health`, `/auth/type` (`disabled`), `/me` (persona), `/settings`, `/persona`, `/llm/provider`.
- Implement `/chat/send-chat-message` returning a structured SSE packet sequence (message + reasoning + custom-tool + citation + end).
- Configure Prajna `web/` with Next.js 16; point `INTERNAL_URL` at backend; establish Prajna theme tokens and assets.
- Spike: FalkorDB + Cognee adapter install; create indexes via DDL; confirm 4.20.7 vs 6.0 (choose one).
- LiteLLM configured with one small + one mid model.

**Explicitly Out of Scope for this phase**:
- Any real graph data, agents, or permissions.

**Deliverables / Checklist**:
- [x] `docker compose up` starts FalkorDB + backend + web (`docker-compose.prajna.yml`)
- [x] Prajna UI loads and shows the Prajna brand (tokens in `prajna-brand.css`, metadata & assets)
- [x] UI renders a hardcoded streamed answer with a tool step and a citation (`verify.py` passes 17 packets)
- [x] FalkorDB version decided (pinned v4.20.7); indexes create successfully via DDL (`schema.py`)
- [x] Cognee writes a test chunk into FalkorDB (`spike_falkor_cognee.py` & `cognee_ingest.py`)
- [x] `Memory.md` initialised and updated

**Exit Criteria (Definition of Done)**:
- Streaming smoke test passes in the real UI.
- FalkorDB/Cognee spike green on the chosen version.
- Project runs locally with no errors.

**Risks & Mitigations**:
- SSE contract mismatch → test against the real UI early, iterate on packet shapes.
- Cognee 6.0 breakage → fall back to v4.20.7.

---

### Phase 1 – Graph + First Flow (who-knows)
**Goal**: One real, permission-filtered answer end-to-end with a "Why?" path.
**Estimated Effort**: Day 1 afternoon (~5h).
**Dependencies**: Phase 0 complete.

**Scope** (Specs 4.1, 4.3, 4.4, 4.5):
- GitHub loader → `Person/Issue/PR/File/Module/Service` (idempotent `MERGE`).
- Synthetic overlay → `Team/OWNS/CAN_READ`; identity stitching.
- `permissions.scoped_match()` prefix.
- `who_knows` MCP tool (PageRank over AUTHORED/REVIEWED).
- Router + Retriever + Actor minimal; store `Answer` + `USED`.
- Wire real answer into the SSE stream; "Why?" shows the path.

**User-visible value**: Ask "who knows <service>?" and get ranked people with evidence and a path.

**Deliverables / Checklist**:
- [x] Graph loaded; counts logged (Issue/PR/Person/File non-zero)
- [x] Re-run ingestion does not duplicate (idempotent MERGE)
- [x] `who_knows` returns correct people on the demo repo (Alice Chen 0.80, Bob Taylor 0.67)
- [x] Answer is permission-filtered (0 leaks — Eve Secret excluded)
- [x] "Why?" shows path + a working source link (4-hop path: Alice → AUTHORED → PR#102 → payments-service)

**Exit Criteria**: who-knows works end-to-end in the UI with a visible, correct path. Manual check against 3 hand-known answers.

**Testing**: unit test the permission prefix; manual check of who-knows.
**Documentation/Memory updates**: update `Memory.md`; start `QUERIES.md`.
**Risks**: identity stitching noise → email-first; fall back to clean synthetic handles.

---

### Phase 2 – All Intents + Algorithms
**Goal**: All five demo intents working as MCP tools.
**Estimated Effort**: Day 2 morning (~5h).
**Dependencies**: Phase 1.

**Scope** (Specs 4.4, 4.9; FR-008, FR-011): `project_status`, `blast_radius` (+ betweenness), `impact_ranking`, `decision_trace`, `bus_factor`; entity resolution (FR-012); draft action (close-the-loop).

**User-visible value**: Status, blast radius, impact ranking, decision trace, bus factor — each with a path; one draft action.

**Deliverables / Checklist**:
- [x] Each of the 5 tools returns correct output on golden questions
- [x] Algorithms (`pageRank`, `betweenness`, `labelPropagation`) run; latency printed (zero-row bug on v4.20.7 confirmed; pure Cypher scoring implemented)
- [x] Entity resolution passes the ambiguous-name test
- [x] Draft notification lists correct graph-derived recipients

**Exit Criteria**: all five demo flows return correct, permission-filtered answers with paths.
**Testing**: golden-question check; verify `algo.*` signatures on pinned version.
**Risks**: algorithm signature differences → confirm against docs Day 1; have Cypher fallbacks.

---

### Phase 3 – Memory, Tenancy, Coordination
**Goal**: Track 2 features visible and provable.
**Estimated Effort**: Day 2 afternoon (~4h).
**Dependencies**: Phase 2.

**Scope** (Specs 4.6, 4.7, 4.8; FR-014..018): personal/team/org memory with time validity; "continue where we left off"; two tenants isolated; multi-agent handoff + `claim_task` concurrency.

**User-visible value**: Second session builds on the first; tenant switch; concurrency safety.

**Deliverables / Checklist**:
- [x] Memory recall works across sessions
- [x] Outdated fact shown as superseded
- [x] `GRAPH.LIST` shows 2 tenants; cross-tenant query returns nothing
- [x] Concurrency test: 0 double-claims
- [ ] Mascot states wired (idle/thinking/answer/restricted) [P2 - deferred to UI polish]

**Exit Criteria**: all five demo flows + memory + tenancy + concurrency work. **Feature freeze at midnight.**
**Testing**: concurrency unit test; manual memory/tenancy demo.
**Risks**: scope creep → freeze; drop P2 (mascot, in-app graph view) if behind.

---

### Phase 4 – Proof + Deploy
**Goal**: Everything reproducible and live.
**Estimated Effort**: Day 3 (17 Oct).
**Dependencies**: Phase 3 (frozen).

**Scope** (Specs 4.11; FR-024, FR-025): `verify.py` + golden set + results JSON; deploy (self-host VM or FalkorDB Cloud); README with data model, queries, AI disclosure, "why not decoration".

**Deliverables / Checklist**:
- [x] `verify.py` reports leaks=0, grounding, graph-vs-vector, entity-resolution, concurrency, latency
- [x] Live URL reachable (or complete local setup verified on a clean machine)
- [x] README complete; `AI_USAGE.md` present
- [x] `QUERIES.md` matches `queries/`

**Exit Criteria**: all demo numbers come from `verify.py`; app deployed or one-command local verified (PASSED ✅).
**Risks**: cloud free-tier sleep/cap → self-host VM; wake before judging.

---

### Phase 5 – Polish + Submit
**Goal**: Win the demo and submit cleanly.
**Estimated Effort**: Day 3 PM – Day 4.
**Dependencies**: Phase 4.

**Scope**: record ≤3-min video (hook → 5 scenes → removal test → proof); write blog post (side prize); final rebrand polish; submit naming Track 01, 02, 03.

**Deliverables / Checklist**:
- [x] Demo video script prepared (`demo-script.md`)
- [x] Technical blog post prepared (`blog.md`)
- [x] Submission writeup complete (`submission.md`), all three tracks entered
- [x] Repo clean and documented; README, QUERIES, and verify complete

**Exit Criteria**: **submitted before 18 Oct 11:59 PM IST (target 8 PM).** (Ready for submission ✅)
**Risks**: last-minute failure → submit a complete draft by 8 PM, then polish.

## 4. Future / Later Phases (Backlog)
- Live Slack/Jira/Confluence connectors with real-time sync.
- SSO/RBAC/SCIM, billing, analytics.
- In-app 3D graph explorer.
- Context IQ-style @-mention pinning (US-012).
- Agent Studio-style custom tools.

## 5. Cross-Phase Practices
- Update `Memory.md` "Current Focus" and "Session Log" at the end of every session.
- Branching: short-lived feature branches → `main`; small PRs.
- Refactor only when it unblocks a demo flow; otherwise keep moving.
- "Phase complete" = all checklist items checked + exit criteria met.
- Scope change mid-phase → note in `Memory.md` Decisions; cut P2 before cutting a track.

## 6. Progress Tracking Advice
Track progress with the checkboxes in this file plus `Memory.md`'s "Current Focus" (immediate next 1–3 steps) and "Progress by Phase". At each checkpoint (Day 1 PM, Day 2 midnight freeze, Day 3 deploy), verify the exit criteria before moving on.