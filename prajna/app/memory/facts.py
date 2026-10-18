import uuid
from typing import Any, Dict, List, Optional
from prajna.app.graph.falkor_client import falkor_client

class FactStore:
    def upsert_fact(self, text: str, subject: str, tenant: str = "kirana") -> str:
        fact_id = f"fact:{uuid.uuid4().hex[:8]}"
        # Invalidate old facts about subject (valid_to is set)
        supersede_cypher = """
        MATCH (f:Fact {subject: $subject})
        WHERE f.valid_to IS NULL
        SET f.valid_to = datetime()
        """
        falkor_client.query(supersede_cypher, {"subject": subject}, tenant=tenant)

        # Insert new current fact
        insert_cypher = """
        CREATE (f:Fact {
            id: $fact_id,
            subject: $subject,
            text: $text,
            valid_from: datetime(),
            valid_to: null
        })
        RETURN f.id
        """
        falkor_client.query(insert_cypher, {"fact_id": fact_id, "subject": subject, "text": text}, tenant=tenant)
        return fact_id

    def get_current_facts(self, subject: Optional[str] = None, tenant: str = "kirana") -> List[Dict[str, Any]]:
        if subject:
            cypher = """
            MATCH (f:Fact {subject: $subject})
            WHERE f.valid_to IS NULL
            RETURN f.id, f.subject, f.text, f.valid_from
            """
            rows = falkor_client.query(cypher, {"subject": subject}, tenant=tenant)
        else:
            cypher = """
            MATCH (f:Fact)
            WHERE f.valid_to IS NULL
            RETURN f.id, f.subject, f.text, f.valid_from
            """
            rows = falkor_client.query(cypher, {}, tenant=tenant)
        return [{"id": r[0], "subject": r[1], "text": r[2], "valid_from": r[3]} for r in rows]

fact_store = FactStore()
