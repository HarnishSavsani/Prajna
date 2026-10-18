// Caller: ActorAgent | Params: $user_id, $target
// Purpose: Multi-hop recipient resolution for shipped fixes to close the loop

MATCH (i:Issue)
WHERE toLower(i.id) CONTAINS toLower($target) OR toLower(i.title) CONTAINS toLower($target)
OPTIONAL MATCH (pr:PR)-[:FIXES]->(i)
OPTIONAL MATCH (rel:Release)-[:CONTAINS]->(pr)
OPTIONAL MATCH (tk:Ticket)-[:ESCALATED_TO]->(i)
OPTIONAL MATCH (reporter:Person)-[:REPORTED]->(tk)

RETURN i.id AS issue_id,
       i.title AS issue_title,
       rel.id AS release_tag,
       pr.title AS pr_title,
       collect(DISTINCT reporter.display_name) AS affected_recipients,
       collect(DISTINCT tk.title) AS tickets_resolved
