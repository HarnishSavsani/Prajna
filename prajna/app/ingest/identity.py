from typing import Any, Dict, List
from prajna.app.graph.falkor_client import falkor_client

def stitch_identity(canonical_id: str, display_name: str, email: str, github_handle: str = "", slack_handle: str = "", tenant: str = "kirana") -> None:
    """
    Consolidates multiple external tool handles into a single Person node in FalkorDB.
    """
    cypher = """
    MERGE (p:Person {id: $canonical_id})
    SET p.display_name = $display_name,
        p.email = $email,
        p.github_handle = $github_handle,
        p.slack_handle = $slack_handle
    """
    falkor_client.query(cypher, {
        "canonical_id": canonical_id,
        "display_name": display_name,
        "email": email,
        "github_handle": github_handle,
        "slack_handle": slack_handle
    }, tenant=tenant)
