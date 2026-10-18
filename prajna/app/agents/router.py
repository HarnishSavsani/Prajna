import re
from typing import Any, Dict, Tuple

class RouterAgent:
    """
    Classifies intent and extracts target entities without relying on external fragile LLM calls
    for deterministic, fast (<5ms) tool selection.
    """
    def route(self, query: str) -> Tuple[str, Dict[str, Any]]:
        q = query.lower()

        # Intent: bus factor
        if "bus factor" in q or "single maintainer" in q or "single point of failure" in q:
            target = self._extract_target(q, ["bus factor of", "bus factor for", "bus factor"])
            return "bus_factor", {"target": target or "*"}

        # Intent: who knows / expertise
        if "who knows" in q or "who understands" in q or "expert" in q or "worked on" in q:
            target = self._extract_target(q, ["who knows", "who understands", "expert on", "expert in", "worked on"])
            return "who_knows", {"target": target or "payments"}

        # Intent: blast radius / dependency
        if "blast radius" in q or "breaks if" in q or "depends on" in q or "dependency" in q:
            target = self._extract_target(q, ["blast radius of", "breaks if", "depends on", "blast radius"])
            return "blast_radius", {"target": target or "payments"}

        # Intent: project status
        if "status of" in q or "project status" in q or "progress on" in q:
            target = self._extract_target(q, ["status of", "project status of", "progress on"])
            return "project_status", {"target": target or "checkout"}

        # Intent: customer impact ranking
        if "impact" in q or "complaints" in q or "most complained" in q:
            target = self._extract_target(q, ["impact of", "complaints about"])
            return "impact_ranking", {"target": target or "*"}

        # Intent: decision trace
        if "why did we" in q or "decision" in q or "rationale" in q:
            target = self._extract_target(q, ["decision on", "why did we", "rationale for"])
            return "decision_trace", {"target": target or "decision:1"}

        # Intent: close the loop action
        if "close the loop" in q or "notify customers" in q or "shipped fix" in q:
            target = self._extract_target(q, ["notify for issue", "close the loop for", "shipped fix"])
            return "draft_close_the_loop", {"target": target or "issue:101"}

        # Default fallback
        return "who_knows", {"target": "payments"}

    def _extract_target(self, text: str, triggers: list[str]) -> str:
        stopwords = {"the", "a", "an", "about", "for", "of", "service", "module", "system"}
        for t in triggers:
            if t in text:
                parts = text.split(t, 1)
                if len(parts) > 1:
                    clean = parts[1].strip(" ?.,!\"'")
                    words = [w for w in clean.split() if w not in stopwords]
                    if words:
                        return words[0]
                    words_raw = clean.split()
                    if words_raw:
                        return words_raw[0]
        return ""

router_agent = RouterAgent()
