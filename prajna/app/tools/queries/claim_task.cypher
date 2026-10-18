// Caller: Multi-Agent Coordinator | Params: $task_id, $version, $agent_id
// Purpose: Atomic compare-and-swap task claiming in FalkorDB

MATCH (t:Task {id: $task_id})
WHERE t.status IN ['open', 'routed'] AND t.version = $version
SET t.status = 'claimed',
    t.version = t.version + 1,
    t.claimed_by = $agent_id
MERGE (a:Agent {id: $agent_id})
MERGE (a)-[:CLAIMED]->(t)
RETURN t.id AS id, t.status AS status, t.version AS version, a.id AS agent_id
