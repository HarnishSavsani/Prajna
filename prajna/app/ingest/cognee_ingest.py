from typing import Any, Dict, List
from prajna.app.graph.falkor_client import falkor_client

def ingest_doc_chunk(chunk_id: str, text: str, mentions_ids: List[str] = None, tenant: str = "kirana") -> None:
    """
    Simulates Cognee-style hybrid ingestion of unstructured text directly into FalkorDB
    as a Chunk node connected via MENTIONS relationships.
    """
    cypher = """
    MERGE (c:Chunk {id: $chunk_id})
    SET c.text = $text
    """
    falkor_client.query(cypher, {"chunk_id": chunk_id, "text": text}, tenant=tenant)

    if mentions_ids:
        for mid in mentions_ids:
            link = """
            MATCH (c:Chunk {id: $chunk_id})
            MATCH (n {id: $mid})
            MERGE (c)-[:MENTIONS]->(n)
            """
            try:
                falkor_client.query(link, {"chunk_id": chunk_id, "mid": mid}, tenant=tenant)
            except Exception:
                pass
