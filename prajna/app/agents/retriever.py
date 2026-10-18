from typing import Any, Dict
from prajna.app.tools.mcp_tools import tool_registry

class RetrieverAgent:
    """
    Executes the designated MCP query against FalkorDB, applying permission context.
    """
    def retrieve(self, tool_name: str, params: Dict[str, Any], user_id: str = "person:alice", tenant: str = "kirana") -> Dict[str, Any]:
        full_params = dict(params)
        full_params["user_id"] = user_id
        return tool_registry.execute(tool_name, full_params, tenant=tenant)

retriever_agent = RetrieverAgent()
