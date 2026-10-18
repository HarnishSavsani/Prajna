import logging
from typing import Any, Dict, List, Optional
import falkordb
from prajna.app.config import settings

logger = logging.getLogger(__name__)

class FalkorClient:
    def __init__(self, host: str = settings.FALKORDB_HOST, port: int = settings.FALKORDB_PORT):
        self.host = host
        self.port = port
        self._db: Optional[falkordb.FalkorDB] = None

    @property
    def db(self) -> falkordb.FalkorDB:
        if self._db is None:
            self._db = falkordb.FalkorDB(host=self.host, port=self.port)
        return self._db

    def select_graph(self, tenant: str = settings.DEFAULT_TENANT) -> falkordb.Graph:
        graph_name = f"tenant_{tenant}" if not tenant.startswith("tenant_") else tenant
        return self.db.select_graph(graph_name)

    def query(self, cypher: str, params: Optional[Dict[str, Any]] = None, tenant: str = settings.DEFAULT_TENANT) -> List[Any]:
        g = self.select_graph(tenant)
        result = g.query(cypher, params or {})
        return result.result_set

    def list_graphs(self) -> List[str]:
        try:
            return self.db.list_graphs()
        except Exception as e:
            logger.warning(f"Error listing graphs: {e}")
            return []

falkor_client = FalkorClient()
