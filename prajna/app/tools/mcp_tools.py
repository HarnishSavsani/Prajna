import logging
import os
import time
from typing import Any, Dict, List, Optional
from prajna.app.graph.falkor_client import falkor_client

logger = logging.getLogger(__name__)

class ToolRegistry:
    def __init__(self):
        self.queries_dir = os.path.join(os.path.dirname(__file__), "queries")
        self.tools = {
            "who_knows": "who_knows.cypher",
            "project_status": "project_status.cypher",
            "blast_radius": "blast_radius.cypher",
            "bus_factor": "bus_factor.cypher",
            "impact_ranking": "impact_ranking.cypher",
            "decision_trace": "decision_trace.cypher",
            "draft_close_the_loop": "draft_close_the_loop.cypher",
            "claim_task": "claim_task.cypher",
        }

    def _read_query(self, filename: str) -> str:
        path = os.path.join(self.queries_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def execute(self, tool_name: str, params: Dict[str, Any], tenant: str = "kirana") -> Dict[str, Any]:
        if tool_name not in self.tools:
            raise ValueError(f"Unknown MCP tool: {tool_name}")

        cypher = self._read_query(self.tools[tool_name])
        start_time = time.monotonic()
        raw_rows = falkor_client.query(cypher, params, tenant=tenant)
        latency_ms = round((time.monotonic() - start_time) * 1000, 2)

        # Build explainable graph path representation
        path = self._build_path(tool_name, params, raw_rows)

        return {
            "tool_name": tool_name,
            "latency_ms": latency_ms,
            "raw_rows": raw_rows,
            "path": path,
            "params": params,
        }

    def _build_path(self, tool_name: str, params: Dict[str, Any], rows: List[Any]) -> List[str]:
        target = params.get("target", "")
        if tool_name == "who_knows":
            if rows:
                top_author = rows[0][1] if len(rows[0]) > 1 else "Unknown"
                return [f"{top_author} → AUTHORED → PRs → TOUCHES → Files → PART_OF → {target}"]
            return [f"Query target {target} → No contributors found"]
        elif tool_name == "blast_radius":
            paths = []
            for r in rows:
                if len(r) > 3 and isinstance(r[3], list):
                    paths.append(" → CALLS → ".join(r[3]))
            return paths or [f"Target {target} has 0 downstream callers"]
        elif tool_name == "impact_ranking":
            return [f"Customer Tickets → ABOUT → Feature {target or 'all'}"]
        elif tool_name == "decision_trace":
            return [f"Decision {target} → BASED_ON → Evidence → SUPERSEDES → Prior Decisions"]
        elif tool_name == "draft_close_the_loop":
            return [f"Release → CONTAINS → PR → FIXES → Issue {target} ← ESCALATED_TO ← Tickets ← REPORTED ← Customers"]
        return [f"Tool {tool_name} executed on target {target}"]

tool_registry = ToolRegistry()
