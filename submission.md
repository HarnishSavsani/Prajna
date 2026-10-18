# Graph Hacks 2026 — Final Submission Checklist (`submission.md`)

**Project Name**: Prajna (प्रज्ञा) — Graph-Native "AI Teammate" on FalkorDB  
**Team Name**: Neural Nexus  
**Event**: Graph Hacks 2026 (WeMakeDevs × FalkorDB, 15–18 Oct 2026)  
**Submission Deadline**: 18 Oct 2026 11:59 PM IST (Target: 8:00 PM IST)

---

## 📋 Hackathon Submission Form Fields

| Submission Field | Status / Value | Location / Notes |
|---|---|---|
| **Project Title** | `Prajna: Graph-Native AI Teammate on FalkorDB` | Ready |
| **One-Line Tagline** | `An open-source organizational intelligence work graph built in FalkorDB that delivers explainable multi-hop answers, pre-LLM security, and multi-agent coordination.` | Ready |
| **GitHub Repository URL** | `https://github.com/harnish/prajna` (or target team repo) | Ready to make public & push |
| **Live Deployment URL** | `http://localhost:3000` (Local verified) or Self-Hosted Cloud VM IP | Documented in README |
| **Demo Video Link** | `[PLACEHOLDER: Insert YouTube / Loom Link here]` | Max 3 mins; follow `demo-script.md` |
| **Blog Post Link (Side Prize)** | `[PLACEHOLDER: Insert Dev.to / Medium / Hashnode Link here]` | Content drafted in `blog.md` |
| **Tracks Entered** | **Track 01, Track 02, Track 03** (All Three Tracks) | Explicitly detailed below |

---

## 🎯 Track Selections & Proof Mapping

### Track 01: Agents on Connected Data
- **What We Built**: Multi-agent orchestration loop (`RouterAgent`, `RetrieverAgent`, `HistorianAgent`, `ActorAgent`) executing 8 parameterised Cypher tools over FalkorDB.
- **Key Proof**:
  - `who_knows`: PageRank expertise matching over Git author/reviewer history in **2.2 ms**.
  - `blast_radius`: Multi-hop DAG betweenness analysis across service dependencies in **1.6 ms**.
  - `impact_ranking`: Bipartite graph projection of customer escalations in **1.2 ms**.
  - `decision_trace`: Temporal ADR superseding chain in **1.1 ms**.
  - Persists append-only `(Turn)-[:PRODUCED]->(Answer)-[:USED]->(Evidence)` audit nodes.

### Track 02: Memory & Multi-Agent Coordination
- **What We Built**: Tri-scoped temporal memory (`Episode` and `Fact` nodes with `SCOPE_PERSONAL`, `SCOPE_TEAM`, `SCOPE_ORG` and temporal timestamps), multi-graph tenant isolation (`GRAPH.LIST`), and atomic version-guarded optimistic concurrency control on `Task` nodes (`claim_task`).
- **Key Proof**:
  - `continue_session`: Historian agent recalls personal episodes and active facts in **0.8 ms**.
  - Concurrency test: **0 double-claims** across concurrent agent workers using compare-and-swap Cypher.
  - Multi-tenancy: Separate FalkorDB graph keys (`prajna`, `tenant_globex`) with zero cross-tenant leakage.

### Track 03: Company Brain / Work Graph
- **What We Built**: Unified work graph linking public code repositories (commits, PRs, issues, releases) with synthetic enterprise communication layers (customer support tickets, teams, architecture decisions).
- **Key Proof**:
  - Pre-LLM permission scoping (`permissions.scoped_match()`) guarantees **0 permission leaks** between admin and restricted intern roles.
  - FalkorDB Removal Test: Halting FalkorDB immediately terminates the application, proving the graph is the core engine, not decoration.

---

## 🏆 Pre-Submission Verification Summary (`verify.py`)

Every benchmark metric claimed in the submission is verified and reproducible via `docker exec prajna-backend python verify.py`:

```
=================================================================
          PRAJNA VERIFICATION BENCHMARK CONSOLE TABLE
=================================================================
  Metric                               | Measured Value          
  ---------------------------------------------------------------
  Permission Leaks (Target: 0)         | 0                       
  Grounding Rate                       | 100.0%
  Entity Resolution Accuracy           | 96.7%
  Graph-Native Reasoning Score         | 100.0%
  Vector-Only Baseline Score           | 6.7%
  Concurrency Double-Claims            | 0                       
  Tenant Graph Isolation               | Verified (0 leaks)      
  Latency: who_knows                   | 2.2 ms
  Latency: blast_radius                | 1.6 ms
  Latency: project_status              | 2.3 ms
  Latency: bus_factor                  | 2.0 ms
  Latency: impact_ranking              | 1.2 ms
  Latency: decision_trace              | 1.1 ms
  Latency: draft_close_the_loop        | 1.1 ms
  Latency: continue_session            | 0.8 ms
=================================================================
```

---

## 📁 Repository Integrity Checklist

- [x] **README.md** at repository root (pitch, tracks, quickstart, data model diagram, queries table, architecture, "Why not decoration", benchmark results, team roles).
- [x] **AI_USAGE.md** present (adhering strictly to Hackathon Rules 11–13).
- [x] **QUERIES.md** and **vibe-coding/QUERIES.md** present and synchronized with all 8 `.cypher` files.
- [x] **prajna/verify.py** runs cleanly and exports `prajna/verification_results.json`.
- [x] **prajna/tests/fixtures/golden_questions.json** committed as evaluation baseline.
- [x] **docker-compose.prajna.yml** boots cleanly (`falkordb` v4.20.7 + `prajna-backend` + `web`).
- [x] Zero uncommitted sensitive secrets (`.env` omitted, `.env.example` provided).

---

## 👥 Team Roles & Contributions

- **Harnish Savsani** (`harnish@prajna.ai`) — Lead Architect: FalkorDB Graph Schema, Cypher Algorithms, Pre-LLM Permission Scoping, and Multi-Agent Orchestration.
- **Rohan Gaikwad** (`rohan@prajna.ai`) — Backend & Concurrency: Atomic CAS task claiming (`claim_task`), multi-graph tenant isolation, and SSE streaming pipeline.
- **Ronit Munde** (`ronit@prajna.ai`) — Ingestion & Data Engine: PyGithub pipeline, Cognee adapter integration, and synthetic enterprise overlay generator.
- **Swati Gangurde** (`swati@prajna.ai`) — Frontend & UX Lead: Next.js 16 / React 19 interface, interactive "Why?" graph path drawer, and tenant/persona switcher.
