// Caller: RetrieverAgent | Params: $user_id, $target
// Purpose: Rank features by distinct complaining customers/accounts

MATCH (p:Person)-[:REPORTED]->(tk:Ticket)-[:ABOUT]->(f:Feature)
WHERE $target = '*' OR toLower(f.id) CONTAINS toLower($target) OR toLower(f.name) CONTAINS toLower($target)

WITH f, count(DISTINCT p) AS affected_customers, collect(DISTINCT p.display_name) AS customers, collect(DISTINCT tk.title) AS ticket_titles
RETURN f.id AS feature_id,
       f.name AS feature_name,
       affected_customers,
       customers,
       ticket_titles
ORDER BY affected_customers DESC
LIMIT 5
