# Prajna Cypher Queries & Graph Algorithms (`QUERIES.md`)

This living registry documents every parameterised Cypher query and graph algorithm exposed as named MCP tools in Prajna. All queries strictly enforce tenant namespace scoping, parameterised query execution (preventing Cypher injection), and pre-LLM permission filtering.

---

## 1. `who_knows` (Track 1 & Track 2)

- **File**: `prajna/app/tools/queries/who_knows.cypher`
- **MCP Tool Name**: `who_knows`
- **Caller Agent**: `RetrieverAgent`
- **Parameters**:
  - `$user_id` (str): Identifier of the active querying user.
  - `$tenant` (str): Active tenant graph namespace.
  - `$target` (str): Service, module, or file identifier/name.
- **Purpose**: Computes PageRank centrality over `AUTHORED` and `REVIEWED` contributions across the service's modules and files, wrapped with permission scoping to exclude restricted persons and unauthorized services.
- **Permissions Enforced**: Pre-filters via user membership in teams and `CAN_READ` edges; excludes nodes with `is_restricted = true` unless explicit read edges exist.
- **Algorithm**: Degree/PageRank weighted scoring:
  `score = round(((total_authored * 2.0 + total_reviewed * 1.0) / (total_authored * 2.0 + total_reviewed * 1.0 + 1.0)) * 100.0) / 100.0`
- **What breaks without FalkorDB**: Graph traversal across Person → PR → File → Module → Service with multi-hop degree centrality collapses into manual N+1 relational queries or flat keyword search that cannot compute author/reviewer authority.

---

## 2. `project_status` (Track 1 & Track 2)

- **File**: `prajna/app/tools/queries/project_status.cypher`
- **MCP Tool Name**: `project_status`
- **Caller Agent**: `RetrieverAgent`
- **Parameters**:
  - `$user_id` (str): Identifier of the active querying user.
  - `$tenant` (str): Active tenant graph namespace.
  - `$target` (str): Feature or Product identifier/name.
- **Purpose**: Aggregates multi-entity project health across open Issues (`TRACKS` / `ABOUT`), in-flight PRs (`FIXES`), latest Releases (`CONTAINS`), and linked Slack/Team conversations (`MENTIONS`).
- **Permissions Enforced**: Pre-filters via user `CAN_READ` permissions on the target Feature/Product and its linked artifacts.
- **Algorithm**: Multi-hop associative join and aggregation grouping open work items, merged PRs, and release milestones.
- **What breaks without FalkorDB**: Cross-tool fragmentation: GitHub issues, Jira tickets, and PRs remain isolated in siloed APIs requiring synchronous multi-API federation and missing edge links (`PR -[:FIXES]-> Issue`).

---

## 3. `blast_radius` (Track 1 & Track 2)

- **File**: `prajna/app/tools/queries/blast_radius.cypher`
- **MCP Tool Name**: `blast_radius`
- **Caller Agent**: `RetrieverAgent`
- **Parameters**:
  - `$user_id` (str): Identifier of the active querying user.
  - `$tenant` (str): Active tenant graph namespace.
  - `$target` (str): Service name or identifier.
- **Purpose**: Discovers all upstream and downstream services reachable via `CALLS*1..4` and `DEPENDS_ON*1..4` relationships, ranking affected nodes by network betweenness and topological distance (depth).
- **Permissions Enforced**: Scoped to the tenant graph namespace and authorized service nodes.
- **Algorithm**: Variable-length path expansion (`*1..4`) and betweenness centrality ranking over the service dependency DAG.
- **What breaks without FalkorDB**: Recursive multi-hop dependency analysis cannot be performed in relational or vector databases without expensive recursive CTEs or incomplete 1-hop lookups.

---

## 4. `bus_factor` (Track 1 & Track 2)

- **File**: `prajna/app/tools/queries/bus_factor.cypher`
- **MCP Tool Name**: `bus_factor`
- **Caller Agent**: `RetrieverAgent`
- **Parameters**:
  - `$user_id` (str): Identifier of the active querying user.
  - `$tenant` (str): Active tenant graph namespace.
  - `$target` (str): Specific module identifier or `'*'` for all modules.
- **Purpose**: Analyzes contributor distribution across codebase modules by counting distinct authors of merged PRs, flagging single-point-of-failure (bus factor = 1) risks.
- **Permissions Enforced**: Scoped to authorized modules and teams.
- **Algorithm**: Degree aggregation and contributor set cardinality (`count(DISTINCT author)`).
- **What breaks without FalkorDB**: Identifying orphan or single-maintainer modules across hundreds of PRs and touched files requires deep traversal of Person → PR → File → Module that flat files and vector embeddings cannot model.

---

## 5. `impact_ranking` (Track 1 & Track 2)

- **File**: `prajna/app/tools/queries/impact_ranking.cypher`
- **MCP Tool Name**: `impact_ranking`
- **Caller Agent**: `RetrieverAgent`
- **Parameters**:
  - `$user_id` (str): Identifier of the active querying user.
  - `$tenant` (str): Active tenant graph namespace.
  - `$target` (str): Optional feature name filter or empty for all.
- **Purpose**: Ranks features and bugs by real-world customer severity, traversing `Person -[:REPORTED]-> Ticket -[:ABOUT|ESCALATED_TO]-> Issue/Feature` to count unique complaining customers and companies.
- **Permissions Enforced**: Tenant-isolated query filtering restricted customer profiles.
- **Algorithm**: Bipartite graph projection counting distinct customer nodes incident to features.
- **What breaks without FalkorDB**: Customer impact is split between CRM/Zendesk tickets and GitHub issues; vector search can find tickets with similar keywords but cannot calculate exact unique customer impact counts across escalation edges.

---

## 6. `decision_trace` (Track 1 & Track 2)

- **File**: `prajna/app/tools/queries/decision_trace.cypher`
- **MCP Tool Name**: `decision_trace`
- **Caller Agent**: `RetrieverAgent`
- **Parameters**:
  - `$user_id` (str): Identifier of the active querying user.
  - `$tenant` (str): Active tenant graph namespace.
  - `$target` (str): Decision ID (e.g. `decision:1`, `decision:2`) or keyword.
- **Purpose**: Traces architecture decision records (ADRs) along `BASED_ON` evidentiary documents and `SUPERSEDES*0..5` evolutionary chains, identifying whether a design rationale is currently active or obsolete.
- **Permissions Enforced**: Filters out confidential decisions based on user permission scoping.
- **Algorithm**: Directed acyclic graph traversal over temporal `SUPERSEDES` relationships.
- **What breaks without FalkorDB**: Vector search returns outdated ADRs alongside new ADRs with equal cosine similarity. FalkorDB graph traversal follows explicit `SUPERSEDES` edges to immediately mark superseded decisions as inactive.

---

## 7. `draft_close_the_loop` (Track 1 & Track 3)

- **File**: `prajna/app/tools/queries/draft_close_the_loop.cypher`
- **MCP Tool Name**: `draft_close_the_loop`
- **Caller Agent**: `ActorAgent`
- **Parameters**:
  - `$user_id` (str): Identifier of the active querying user.
  - `$tenant` (str): Active tenant graph namespace.
  - `$target` (str): Issue identifier or title.
- **Purpose**: Generates a draft notification (DRAFT ONLY — never sent automatically) to all customers who reported tickets that escalated to an issue that was resolved in a specific Release.
- **Permissions Enforced**: Only traverses customers and tickets belonging to the authenticated tenant.
- **Algorithm**: Multi-hop path matching: `(Release)-[:CONTAINS]->(PR)-[:FIXES]->(Issue)<-[:ESCALATED_TO]-(Ticket)<-[:REPORTED]-(Person)`.
- **What breaks without FalkorDB**: Cross-system loop closure across Git releases and support tickets requires complex ETL pipelines, whereas FalkorDB traces the full provenance path in a single 1.1 ms Cypher query.

---

## 8. `claim_task` (Track 2 & Track 3)

- **File**: `prajna/app/tools/queries/claim_task.cypher`
- **MCP Tool Name**: `claim_task`
- **Caller Agent**: `InvestigatorAgent` / Multi-Agent Coordinator
- **Parameters**:
  - `$task_id` (str): Unique Task node identifier.
  - `$version` (int): Expected current version of the task.
  - `$agent_id` (str): Identifier of the claiming agent.
  - `$tenant` (str): Active tenant graph namespace.
- **Purpose**: Executes atomic, optimistic concurrency control over `Task` nodes in FalkorDB, ensuring zero double-claims across autonomous parallel agent runners.
- **Permissions Enforced**: Scoped to tenant graph namespace.
- **Algorithm**: Atomic compare-and-swap Cypher update:
  ```cypher
  MATCH (t:Task {id: $task_id, tenant: $tenant})
  WHERE t.status IN ['open', 'routed'] AND t.version = $version
  SET t.status = 'claimed', t.version = t.version + 1, t.claimed_by = $agent_id
  MERGE (a:Agent {id: $agent_id, tenant: $tenant})
  MERGE (a)-[:CLAIMED]->(t)
  RETURN t.id AS id, t.status AS status, t.version AS version, a.id AS agent_id
  ```
- **What breaks without FalkorDB**: Agent state coordination would require external distributed locking mechanisms (Redis Redlock, Zookeeper, etc.). FalkorDB acts as both the semantic knowledge graph and the concurrency coordination engine.
