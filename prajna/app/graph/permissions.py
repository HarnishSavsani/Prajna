"""
Shared permission-scoping prefix for Cypher queries.
Pre-filters in Cypher before data reaches the LLM.
"""

def scoped_match_prefix() -> str:
    return """
    MATCH (u:Person {id: $user_id})
    OPTIONAL MATCH (u)-[:MEMBER_OF]->(t:Team)-[:CAN_READ]->(allowed_via_team)
    OPTIONAL MATCH (u)-[:CAN_READ]->(allowed_direct)
    WITH u, collect(DISTINCT allowed_via_team) + collect(DISTINCT allowed_direct) AS allowed_nodes
    """

def is_node_allowed_predicate(target_node_alias: str) -> str:
    return f"""(
        NOT coalesce({target_node_alias}.is_restricted, false)
        OR {target_node_alias} IN allowed_nodes
    )"""
