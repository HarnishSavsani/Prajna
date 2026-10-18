import datetime
import uuid
from typing import Any, Dict, List, Optional
from prajna.app.graph.falkor_client import falkor_client

class EpisodeStore:
    def record_episode(self, user_id: str, summary: str, scope: str = "personal", tenant: str = "kirana") -> str:
        ep_id = f"episode:{uuid.uuid4().hex[:8]}"
        cypher = """
        MERGE (u:Person {id: $user_id})
        CREATE (e:Episode {
            id: $ep_id,
            summary: $summary,
            scope: $scope,
            created_at: datetime()
        })
        CREATE (e)-[:SCOPE_PERSONAL]->(u)
        RETURN e.id
        """
        falkor_client.query(cypher, {"user_id": user_id, "ep_id": ep_id, "summary": summary, "scope": scope}, tenant=tenant)
        return ep_id

    def get_recent_episodes(self, user_id: str, limit: int = 3, tenant: str = "kirana") -> List[Dict[str, Any]]:
        cypher = """
        MATCH (u:Person {id: $user_id})<-[:SCOPE_PERSONAL]-(e:Episode)
        RETURN e.id AS id, e.summary AS summary, e.created_at AS created_at
        ORDER BY e.created_at DESC
        LIMIT $limit
        """
        rows = falkor_client.query(cypher, {"user_id": user_id, "limit": limit}, tenant=tenant)
        return [{"id": r[0], "summary": r[1], "created_at": r[2]} for r in rows]

episode_store = EpisodeStore()
