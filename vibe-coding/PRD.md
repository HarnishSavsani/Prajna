
<!-- Generated with detailed vibe-coding PRD prompt. Review assumptions and open questions carefully. -->

# Prajna – Product Requirements Document

**Status**: Complete
**Last Updated**: 2026-10-18
**Owner**: Team Prajna
**Version**: 1.0

---

## 1. Overview

Prajna is an open-source, graph-native "AI teammate" that builds a live knowledge graph of how an organisation actually works — its people, teams, product parts, work items, and knowledge drawn from GitHub, Slack, Jira, and Confluence — in **FalkorDB**, and lets anyone ask questions in natural language. It is for software and product teams (20–500 people) who need answers that live in the *connections* between tools, not inside any single document. It matters now because enterprise AI leaders (DevRev Computer, Microsoft Work IQ) have proven that AI assistants need a "work graph", yet every such product is closed and expensive. **Core value proposition in one sentence: Prajna answers organisational questions with a traceable graph path, respects who is allowed to see what, remembers across sessions, and takes action — all on a graph that is the product, not a side index.**

This PRD is the single source of truth for the Graph Hacks 2026 hackathon build (WeMakeDevs × FalkorDB, 15–18 Oct 2026) and is written so an AI coding agent can implement the system with minimal clarification.

## 2. Problem Statement

The answer to most real workplace questions is not in one document — it lives in the relationships between people, teams, code, tickets, decisions, and conversations, which are scattered across disconnected tools.

- **What pain exists today:** To answer "who knows the Payments service now that its author left?", a developer must cross-reference GitHub commit history, Slack on-call threads, and Jira ownership by hand. To answer "why did we drop Redis for sessions?", the reasoning is split across a Confluence page, a Slack thread, and a pull request.
- **Who feels this pain:** Engineers, engineering managers, product managers, support leads, and new joiners in any multi-tool software organisation.
- **How people solve it today (and fail):** They ask around in Slack and wait hours; they sit through status meetings; they export tickets to spreadsheets. Traditional document search tools retrieve single text documents but cannot reason over relationships, run graph algorithms (expertise, criticality, bus factor), or trace multi-hop paths. They also frequently ignore per-tool permissions.
- **Cost of the problem:** Hours of senior-engineer time per week per team; slow incident response; knowledge lost when people leave; onboarding measured in weeks.

This problem statement is based on the team's direct experience building developer tools and on public descriptions of DevRev Computer and Microsoft Work IQ; specific per-company metrics are assumptions until validated.

## 3. Target Users & Personas

### Primary Persona
- **Name:** Riya Sharma
- **Role / demographics:** Backend engineer, 3 years' experience, on the Payments team at a 120-person SaaS company.
- **Goals:** Find the right person to ask; understand why code was built a certain way; avoid breaking things she doesn't own.
- **Frustrations:** The service author left; nobody documents decisions; Slack search is useless after a week.
- **Tech savviness:** High.
- **Jobs-to-be-Done:**
  - When I pick up an unfamiliar service, I want to see who knows it best, so I can ask the right person first.
  - When I change a shared function, I want to know what depends on it, so I don't cause an incident.
  - When I question a past design, I want to see the decision and its sources, so I understand the rationale.

### Secondary Persona
- **Name:** Arjun Mehta
- **Role:** Engineering manager, owns the payments migration.
- **Goals:** Know real status and blockers without a meeting; spot single-points-of-failure (bus factor).
- **Frustrations:** Status is spread across Jira, Slack, and GitHub; "bus factor" is invisible until someone resigns.
- **Tech savviness:** High.
- **Jobs-to-be-Done:**
  - When I need project status, I want it assembled from tickets, PRs, and chat, so I can skip the status meeting.
  - When I plan staffing, I want to see which modules only one person understands, so I can de-risk.

### Secondary Persona
- **Name:** Kabir Rao
- **Role:** Support lead.
- **Jobs-to-be-Done:** When a complaint arrives, I want to know if it's a known bug and whether the fix shipped, so I can tell the customer accurately and notify everyone affected.

### Anti-Persona (who this is NOT for)
- Individuals wanting a simple personal note chatbot over local markdown files.
- Large enterprises needing SSO, SCIM, billing, and compliance certifications on day one.
- Non-technical teams with no GitHub/Jira/Slack footprint.

## 4. Goals & Success Metrics

### Primary Goals
1. Qualify cleanly for Graph Hacks 2026: FalkorDB is the only database and is provably central.
2. Be competitive in all three tracks (Agents on connected data; Memory and coordination; Company brain).
3. Deliver a demo understandable within 10 seconds and complete within 3 minutes.
4. Make every demo claim reproducible via a verification harness.
5. Showcase FalkorDB's differentiated strengths (graph algorithms, multigraph tenancy, traversal latency, graph+vector in one store, MCP).

### Success Metrics (measurable)
| Metric | Target | Measurement Method | Timeframe |
|---|---|---|---|
| Permission leaks in answers/citations | 0 | `verify.py` leak test (N questions × each role) | By submission (18 Oct) |
| Track focus bullets with a working demoed feature | 15 / 15 | Manual check vs track-mapping table | By submission |
| End-to-end answer latency (demo dataset) | < 4 s typical | In-app timing | By submission |
| Per-tool graph query latency (demo dataset) | < 50 ms typical | In-app timing badge | By submission |
| Golden-question answer correctness | ≥ 24 / 30 | `verify.py` vs hand-labelled answers | By submission |
| Demo video length | ≤ 3 min | Final video | By submission |
| Removal test (stop FalkorDB → product unusable) | Passes | Recorded in video | By submission |

### Guardrail Metrics (must not get worse)
- Zero real messages sent (actions remain drafts only).
- Zero real personal/private data ingested (public + synthetic only).
- Cold-start demo setup remains a single `docker compose up`.

### Non-Goals (explicitly out of scope for this version)
- Real-time sync / webhooks (batch ingestion only).
- SSO, SCIM, billing, usage analytics.
- Voice mode, desktop app, Chrome extension, mobile app.
- Deep research, code sandbox, image generation (out of scope for core graph sprint).
- Sending real emails/Slack messages.
- Training or fine-tuning ML models.
- Ingesting real private company data.

## 5. User Stories / Core Use Cases

### P0 – Must Have (MVP)

**US-001**: As an engineer, I want to ask who knows a service so that I can contact the right person first.
**Acceptance Criteria**:
- Given a service that exists in the graph and the user is permitted to see it
- When the user asks "who knows <service>?"
- Then the system returns people ranked by graph-derived expertise (PageRank over authored/reviewed edges)
- And each person is backed by visible evidence (PRs/reviews) and a "Why?" path.

**US-002**: As an engineer, I want to know what depends on a service so that I avoid breaking things.
**Acceptance Criteria**:
- Given a service with dependency edges
- When the user asks "what breaks if <service> changes?"
- Then the system returns affected services via multi-hop traversal
- And ranks them by criticality (betweenness centrality).

**US-003**: As a manager, I want project status assembled across tools so that I can skip the status meeting.
**Acceptance Criteria**:
- Given a feature/project linked to issues, PRs, releases, and messages
- When the user asks "what's the status of <project>?"
- Then the system returns open issues, in-flight PRs, latest release, and blockers
- And every item is permission-filtered and cited.

**US-004**: As any user, I want every answer to show its reasoning path so that I can trust and verify it.
**Acceptance Criteria**:
- Given any answer
- When the user clicks "Why?"
- Then the system shows the natural-language steps, the graph path, and clickable source links
- And the path corresponds to a stored `Answer` node with the executed Cypher.

**US-005**: As a security lead, I want restricted documents to stay hidden from unauthorised users so that sensitive data never leaks.
**Acceptance Criteria**:
- Given a document readable only by a specific team
- When an unauthorised user asks about it
- Then the system returns "you don't have access" and no restricted node appears in the answer or citations
- And the leak test reports 0 leaks across all roles.

**US-006**: As a returning user, I want Prajna to remember my previous session so that I can continue where I left off.
**Acceptance Criteria**:
- Given a prior session produced personal memory (episodes/facts)
- When the user says "continue where we left off"
- Then the system recalls the prior context and builds on it.

**US-007**: As a platform admin, I want each organisation's data isolated so that tenants never see each other's graph.
**Acceptance Criteria**:
- Given two tenants loaded as separate FalkorDB graphs
- When a query runs in tenant A
- Then no tenant-B node is ever returned
- And `GRAPH.LIST` shows both tenant graphs.

**US-008**: As the system, I want multiple agents to hand off work via shared graph state so that coordination is reliable.
**Acceptance Criteria**:
- Given a `Task` node with status "open" and version N
- When two agents attempt to claim it concurrently
- Then exactly one succeeds (version check) and the other picks another task.

### P1 – Should Have

**US-009**: As a support lead, I want to know if a complaint is a known bug and whether its fix shipped so that I can inform the customer.
**Acceptance Criteria**:
- Given a complaint linked (directly or via duplicate) to an issue fixed by a released PR
- When the user asks about the complaint
- Then the system reports the known issue, the fixing PR, and the release
- And drafts a notification to every affected customer.

**US-010**: As a user, I want ambiguous names resolved to the right entity so that answers are accurate.
**Acceptance Criteria**:
- Given a term matching a product/feature/service name (e.g., "Browser" → "FalkorDB Browser")
- When the user asks about it
- Then the system scopes the answer to that entity, not the generic phrase.

**US-011**: As a PM, I want features ranked by customer complaint volume so that I prioritise correctly.
**Acceptance Criteria**:
- Given tickets linked to features
- When the user asks "which features cause the most complaints?"
- Then the system returns features ranked by distinct complaining customers.

### P2 – Could Have / Nice to Have

**US-012**: As a user, I want to @-mention a specific node to pin it into my prompt (Context IQ-style).

**US-013**: As a viewer, I want a small visual of the graph path, so I can see the connections.

**US-014**: As a user, I want the assistant's avatar (mascot) to reflect state (thinking, answering, restricted), so the UI feels alive.

## 6. Functional Requirements

### Ingestion & Graph Build
- **FR-001**: The system shall ingest GitHub issues, PRs, reviews, releases, file paths, and commit authors for configured public repositories.
- **FR-002**: The system shall ingest unstructured text (docs, discussions, markdown) via Cognee into FalkorDB as `Chunk` nodes with embeddings and `MENTIONS` edges.
- **FR-003**: The system shall load a synthetic organisation overlay (teams, ownership, roles, permissions, private docs).
- **FR-004**: The system shall perform all ingestion idempotently using `MERGE` so re-runs do not duplicate nodes or edges.
- **FR-005**: The system shall stitch a person's multiple tool identities (GitHub, Slack, Jira) into a single `Person` node using email-first then handle heuristics.
- **FR-006**: On re-sync, the system shall mark changed facts' `valid_to` and insert new facts (knowledge currency).
- **FR-007**: The system shall create name/id, full-text, and vector indexes on first run using DDL syntax compatible with FalkorDB 4.x and 6.x.

### Retrieval & Reasoning
- **FR-008**: The system shall answer the intents: status, who-knows, impact/ranking, why/decision-trace, and dependency/blast-radius.
- **FR-009**: The system shall start every retrieval query from the current user and traverse only nodes reachable via `CAN_READ` edges, filtering before any data reaches the LLM.
- **FR-010**: The system shall expose named Cypher/algorithm queries as MCP tools and select among them per question.
- **FR-011**: The system shall compute expertise (PageRank), criticality (betweenness), real teams (label propagation), and bus factor (distinct-contributor count) as agent tools.
- **FR-012**: The system shall resolve a mentioned entity name to the matching graph node when one exists.
- **FR-013**: The system shall store an `Answer` node containing the executed Cypher and `USED` edges to evidence for every response.

### Memory & Coordination
- **FR-014**: The system shall store memory in three scopes — personal, team, org — as graph nodes/edges.
- **FR-015**: The system shall record episodic, semantic, and procedural memory types.
- **FR-016**: The system shall persist chat sessions and turns in FalkorDB.
- **FR-017**: The system shall coordinate multiple agents via `Task` nodes with an optimistic `version` field; a claim shall succeed only if status is open and version matches.
- **FR-018**: The system shall isolate each tenant as a separate FalkorDB graph; cross-tenant queries shall return nothing.

### Actions
- **FR-019**: The user shall be able to request a draft notification to everyone affected by a shipped fix, computed from the graph.
- **FR-020**: The user shall be able to request a draft issue/ticket from a question.
- **FR-021**: The system shall never send real messages; all actions produce drafts only.

### UI & Verification
- **FR-022**: The system shall serve a responsive web chat UI (Next.js 16 / React 19) via a backend that implements the chat streaming contract (see Architecture/Specs).
- **FR-023**: The user shall be able to view the "Why?" trace (reasoning steps, graph path, citations) for any answer.
- **FR-024**: The system shall provide `verify.py` that outputs JSON and a console table for all success metrics.
- **FR-025**: The system shall run locally via a single `docker compose up` bringing up FalkorDB, backend, and web.

## 7. Non-Functional Requirements

- **Performance**: Typical end-to-end answer < 4 s on the demo dataset; per-tool graph query < 50 ms typical; ingestion of the demo dataset completes in < 10 minutes.
- **Security & Privacy**: Authentication may be set to a demo "disabled" mode with a persona switcher; permission filtering is enforced in Cypher before LLM calls; secrets only in `.env`; no real personal/private data; no secrets logged.
- **Accessibility**: UI retains keyboard navigation and visible focus states; target WCAG 2.1 AA (focus ring, labels, 44×44px touch targets, contrast ≥ 4.5:1 for body text).
- **Reliability / Availability**: For the demo, a single deployment is sufficient; if the LLM or Cognee is unavailable, raw graph query results must still return.
- **Scalability**: Demo dataset under ~100 MB (fits FalkorDB Cloud free tier); architecture supports thousands of isolated tenant graphs in one FalkorDB instance.
- **Usability**: First meaningful answer reachable within two clicks of loading the app; "Why?" available on every answer.
- **Compatibility**: Latest Chrome/Firefox/Safari/Edge; backend Python 3.11–3.13; FalkorDB image pinned (v4.20.7).

## 8. Constraints & Assumptions

### Constraints
- **Technical**: FalkorDB must be the primary graph database and central to the product (hackathon rule); vectors and full-text must use FalkorDB indexes (no second store); Cognee FalkorDB adapter requires Python 3.11–3.13 and FalkorDB on port 6379.
- **Business / time**: Focused build days (15–18 Oct 2026); team of 4.
- **Legal / regulatory**: Only public, synthetic, or own data; actions are drafts only; open source MIT license.
- **Third-party dependencies**: FalkorDB, Cognee + `cognee-community-hybrid-adapter-falkor`, LiteLLM, an LLM provider (e.g., Groq/OpenAI), Prajna web app.

### Assumptions
- **A1**: FalkorDB v4.20.7 is stable with the Cognee adapter.
- **A2**: The multi-packet SSE contract reliably streams answers, reasoning deltas, and tool steps to the web UI.
- **A3**: Slack/Jira/Confluence live API access may be unavailable during the event; synthetic equivalents are acceptable.
- **A4**: FalkorDB's own public repos are an acceptable, recognisable demo dataset.
- **A5**: Per-company ROI/market numbers are illustrative, not researched for this build.
- **A6**: Setting auth to "disabled" with a persona switcher is sufficient for the demo.

## 9. Open Questions & Decisions Needed
1. Which 1–2 public repos form the demo dataset? (Recommended: FalkorDB's own repos.)
2. Do we use live Slack/Jira/Confluence connectors or synthetic equivalents?
3. Deployment target: FalkorDB Cloud free tier vs local compose?
4. Auth model: demo persona switcher enables instant switching between Admin, Engineers, and Restricted users.
5. Confirmation of pinned FalkorDB v4.20.7 runtime stability.

## 10. Appendix

### Glossary
- **Work graph**: a graph of people, teams, parts, work, and knowledge (DevRev/Microsoft term).
- **Part**: a unit of the product — customer-facing (product/capability/feature) or dev-facing (service/module).
- **Identity stitching**: merging a person's accounts across tools into one node.
- **Permission edge**: a `CAN_READ` relationship scoping what a user can retrieve.
- **Removal test**: stopping FalkorDB to prove it is central (hackathon rule 3).
- **Bus factor**: how many people would have to leave before knowledge of a module is lost.

### Competitive landscape (brief)
- **DevRev Computer**: closed, enterprise; Identity·Parts·Work graph; Airdrop sync; personal/team/org memory.
- **Microsoft Work IQ**: closed; Microsoft Graph + semantic index + Data/Memory/Inference work graph.
- **Traditional Search Engines**: search-first over flat vector stores; fails to capture multi-hop relationship reasoning and graph algorithms.
- **Prajna**: open-source, graph-native; FalkorDB is the product, not a side index.

### Inspiration / reference products
DevRev Computer; Microsoft 365 Copilot (Work IQ); Lethe and ClassroomMemory (prior WeMakeDevs × Cognee hackathon winners — one-sentence problem, visible before/after, measured proof).

### Links to existing research/notes
- `graph-hacks-2026-master-notes.md` (hackathon facts, idea history, FalkorDB/Cognee technical notes).
- Companion docs: Architecture.md, Specs.md, Rules.md, Phases.md, Design.md, Memory.md.