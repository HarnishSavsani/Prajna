// Caller: RetrieverAgent | Params: $user_id, $target
// Purpose: Trace decision provenance and superseding chain

MATCH (d:Decision)
WHERE toLower(d.id) CONTAINS toLower($target) OR toLower(d.text) CONTAINS toLower($target)
OPTIONAL MATCH (d)-[:BASED_ON]->(evidence)
OPTIONAL MATCH (d)-[:SUPERSEDES*0..3]->(prior:Decision)

RETURN d.id AS decision_id,
       d.text AS text,
       d.decided_at AS decided_at,
       d.status AS status,
       collect(DISTINCT coalesce(evidence.title, evidence.id)) AS evidence_sources,
       collect(DISTINCT prior.id) AS supersedes_chain
