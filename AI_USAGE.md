# AI Usage & Transparency Disclosure (`AI_USAGE.md`)

This document discloses AI assistant usage for **Prajna**, strictly adhering to **Graph Hacks 2026 Hackathon Rules 11–13** (AI Transparency, Human Design Verification, and Query Explainability).

---

## 1. Hackathon Rule Compliance Summary

- **Rule 11 (AI Transparency)**: Full disclosure of AI coding assistants, foundational models, agentic harnesses, and their respective operational scopes.
- **Rule 12 (Query Explainability)**: Every Cypher query and graph algorithm used by Prajna is human-auditable, parameterised, readable, and documented in `QUERIES.md`. Zero "black-box" or unverified raw Cypher generation.
- **Rule 13 (Human Verification & Architecture)**: Core domain models, architecture designs, optimistic concurrency controls, benchmark fixtures, and security invariants were conceived, reviewed, and validated by human engineers.

---

## 2. AI Assistants & Foundational Models Used

| Tool / Model | Vendor / Framework | Role & Scope of Use |
|---|---|---|
| **Antigravity CLI (agy)** | Google DeepMind / Gemini | Primary agentic coding harness used for task planning, file editing, and test execution workflows. |
| **Gemini 3.8 Flash** | Google DeepMind | Fast multi-step code generation, Cypher query scaffolding, test authoring, and documentation synchronisation. |
| **LiteLLM Engine** | BerriAI | In-app dual-model router: `gpt-4o-mini` (fast entity extraction & tool classification) and `gpt-4o` (explanation & prose generation). |
| **Cognee Hybrid Adapter** | Cognee Community | Unstructured document chunking and FalkorDB graph-entity ingestion pipeline. |

---

## 3. Division of Responsibility: AI vs. Human

### What the Human Engineers Designed and Directed:
1. **Product Concept & Philosophy**: Conceived Prajna as an open-source, graph-native work graph engine ("Work IQ on FalkorDB") where the knowledge graph is the product rather than a secondary vector index.
2. **Schema & Ontology Design**: Authored the C4 architecture, node labels (`Person`, `Service`, `PR`, `Issue`, `Task`, `Episode`, `Fact`), relationship types (`AUTHORED`, `CALLS`, `FIXES`, `SUPERSEDES`, `CLAIMED`), and 18 DDL index definitions.
3. **Security & Permission Model**: Enforced the strict invariant that permissions must be scoped in Cypher (`permissions.scoped_match()`) before data touches the LLM, guaranteeing zero unauthorized data leakage.
4. **Optimistic Concurrency Strategy**: Designed the version-guarded `claim_task` compare-and-swap mechanism in FalkorDB to guarantee 0 double-claims in multi-agent workflows.
5. **30 Golden Questions Benchmark**: Authored the golden benchmark evaluation set in `prajna/tests/fixtures/golden_questions.json` to rigorously test grounding, permission isolation, and entity resolution.
6. **Code Reviews & Sanity Testing**: Manually reviewed all generated Cypher queries, verified Docker Compose container lifecycles, and confirmed zero regression on the live frontend.

### What the AI Assistants Generated & Assisted With:
1. **Boilerplate & Shims**: Generated the FastAPI boot endpoints for the Next.js UI contract (`/health`, `/auth/type`, `/me`, `/settings`, `/chat/send-chat-message`).
2. **SSE Streaming Protocol Adapter**: Implemented the multi-packet SSE generator emitting reasoning deltas, custom tool execution events, and citation markers.
3. **Cypher Query Implementation**: Converted human algorithm specifications (PageRank over PRs, DAG betweenness, temporal superseding) into parameterised `.cypher` scripts.
4. **Test Fixtures & Automation**: Generated test scaffolding, PyGithub loaders, synthetic test overlays (`synthetic_overlay.py`), and the autonomous evaluation harness in `prajna/verify.py`.
5. **Documentation Maintenance**: Kept `Memory.md`, `Phases.md`, `QUERIES.md`, and README aligned across iterative development waves.

---

## 4. Query Explainability & Verification

In accordance with Hackathon Rule 12, **no raw, arbitrary Cypher queries are generated on the fly by an LLM at runtime**. 

Instead:
- The LLM acts solely as a classifier to identify user intent and extract strongly typed parameters (e.g., target entity names).
- The execution layer dispatches to explicit, version-controlled `.cypher` template files located in `prajna/app/tools/queries/`.
- Every query is parameterised (preventing Cypher injection) and human-inspectable.
- The full list of queries, their mathematical/algorithmic rationale, and caller agents are published in [`QUERIES.md`](QUERIES.md).
