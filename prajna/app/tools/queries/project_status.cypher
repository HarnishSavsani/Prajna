// Caller: RetrieverAgent | Params: $user_id, $target
// Purpose: Aggregates open Issues, PRs, and Release info for a target Feature or Service

MATCH (f:Feature)
WHERE toLower(f.id) CONTAINS toLower($target) OR toLower(f.name) CONTAINS toLower($target)
OPTIONAL MATCH (tk:Ticket)-[:ABOUT]->(f)
OPTIONAL MATCH (tk)-[:ESCALATED_TO]->(i:Issue)
OPTIONAL MATCH (pr:PR)-[:FIXES]->(i)
OPTIONAL MATCH (rel:Release)-[:CONTAINS]->(pr)

RETURN f.id AS feature_id,
       f.name AS feature_name,
       collect(DISTINCT i.title) AS issues,
       collect(DISTINCT pr.title) AS prs,
       collect(DISTINCT rel.id) AS releases,
       count(DISTINCT tk) AS ticket_count
