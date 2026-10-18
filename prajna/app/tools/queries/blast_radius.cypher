// Caller: RetrieverAgent | Params: $user_id, $target
// Purpose: Multi-hop service dependency expansion (*1..4) to discover downstream impact

MATCH (origin:Service)
WHERE toLower(origin.id) CONTAINS toLower($target) OR toLower(origin.name) CONTAINS toLower($target)
MATCH path = (dependent:Service)-[:CALLS|DEPENDS_ON*1..4]->(origin)
WHERE origin <> dependent

RETURN dependent.id AS dependent_id,
       dependent.name AS dependent_name,
       length(path) AS depth,
       [n in nodes(path) | n.id] AS dependency_chain
ORDER BY depth ASC
LIMIT 10
