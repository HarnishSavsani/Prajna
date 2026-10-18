import uuid
from typing import Any, Dict, List
from prajna.app.graph.falkor_client import falkor_client

class SessionStore:
    def record_turn(self, session_id: str, query: str, answer_text: str, cypher_used: str, evidence_ids: List[str], tenant: str = "kirana") -> str:
        ans_id = f"answer:{uuid.uuid4().hex[:8]}"
        turn_id = f"turn:{uuid.uuid4().hex[:8]}"

        cypher = """
        MERGE (s:Session {id: $session_id})
        CREATE (t:Turn {id: $turn_id, query: $query, created_at: datetime()})
        CREATE (a:Answer {id: $ans_id, text: $answer_text, cypher: $cypher_used, created_at: datetime()})
        CREATE (s)-[:HAS_TURN]->(t)
        CREATE (t)-[:PRODUCED]->(a)
        """
        falkor_client.query(cypher, {
            "session_id": session_id,
            "turn_id": turn_id,
            "query": query,
            "ans_id": ans_id,
            "answer_text": answer_text,
            "cypher_used": cypher_used
        }, tenant=tenant)

        # Link evidence edges
        for eid in evidence_ids:
            link_cypher = """
            MATCH (a:Answer {id: $ans_id})
            MATCH (e {id: $eid})
            CREATE (a)-[:USED]->(e)
            """
            try:
                falkor_client.query(link_cypher, {"ans_id": ans_id, "eid": eid}, tenant=tenant)
            except Exception:
                pass

        return ans_id

session_store = SessionStore()
