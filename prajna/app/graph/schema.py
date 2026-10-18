import logging
from prajna.app.graph.falkor_client import falkor_client

logger = logging.getLogger(__name__)

DDL_STATEMENTS = [
    "CREATE INDEX FOR (p:Person) ON (p.id)",
    "CREATE INDEX FOR (t:Team) ON (t.id)",
    "CREATE INDEX FOR (s:Service) ON (s.id)",
    "CREATE INDEX FOR (m:Module) ON (m.id)",
    "CREATE INDEX FOR (f:Feature) ON (f.id)",
    "CREATE INDEX FOR (i:Issue) ON (i.id)",
    "CREATE INDEX FOR (pr:PR) ON (pr.id)",
    "CREATE INDEX FOR (tk:Ticket) ON (tk.id)",
    "CREATE INDEX FOR (d:Decision) ON (d.id)",
    "CREATE INDEX FOR (tsk:Task) ON (tsk.id)",
]

def init_schema(tenant: str = "kirana") -> None:
    for stmt in DDL_STATEMENTS:
        try:
            falkor_client.query(stmt, tenant=tenant)
        except Exception as e:
            # Idempotent: Ignore if already exists
            logger.debug(f"Index creation note for '{stmt}': {e}")
