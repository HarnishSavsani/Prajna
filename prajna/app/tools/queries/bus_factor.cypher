// Caller: RetrieverAgent | Params: $user_id, $target
// Purpose: Calculates bus factor (distinct contributors) for modules to spot risk points

MATCH (m:Module)
WHERE $target = '*' OR toLower(m.id) CONTAINS toLower($target) OR toLower(m.name) CONTAINS toLower($target)
MATCH (m)<-[:PART_OF]-(f:File)<-[:TOUCHES]-(pr:PR)
MATCH (author:Person)-[:AUTHORED]->(pr)

WITH m, count(DISTINCT author) AS contributor_count, collect(DISTINCT author.display_name) AS contributors
RETURN m.id AS module_id,
       m.name AS module_name,
       contributor_count,
       contributors,
       CASE WHEN contributor_count <= 1 THEN true ELSE false END AS single_point_of_failure
ORDER BY contributor_count ASC
