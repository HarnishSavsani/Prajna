// Caller: RetrieverAgent | Params: $user_id, $target
// Purpose: Rank people with expertise on a target Service/Module via contribution PageRank proxy

MATCH (svc:Service)
WHERE toLower(svc.id) CONTAINS toLower($target) OR toLower(svc.name) CONTAINS toLower($target)
MATCH (svc)<-[:PART_OF]-(m:Module)<-[:PART_OF]-(f:File)<-[:TOUCHES]-(pr:PR)
MATCH (author:Person)-[:AUTHORED]->(pr)
WHERE NOT coalesce(author.is_restricted, false)

WITH author, svc, count(DISTINCT pr) AS total_authored
OPTIONAL MATCH (author)-[:REVIEWED]->(pr2:PR)-[:TOUCHES]->(f2:File)-[:PART_OF]->(:Module)-[:PART_OF]->(svc)
WITH author, svc, total_authored, count(DISTINCT pr2) AS total_reviewed
WITH author, svc, total_authored, total_reviewed,
     round(((total_authored * 2.0 + total_reviewed * 1.0) / (total_authored * 2.0 + total_reviewed * 1.0 + 1.0)) * 100.0) / 100.0 AS score

RETURN author.id AS person_id,
       author.display_name AS name,
       score,
       total_authored AS authored_prs,
       total_reviewed AS reviewed_prs,
       svc.id AS service_id,
       svc.name AS service_name
ORDER BY score DESC
LIMIT 5
