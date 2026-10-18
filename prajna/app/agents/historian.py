from typing import Any, Dict, List
from prajna.app.memory.episodes import episode_store
from prajna.app.memory.facts import fact_store

class HistorianAgent:
    """
    Recalls personal episodes and current facts on new sessions to provide contextual awareness.
    """
    def recall(self, user_id: str, subject: str = None, tenant: str = "kirana") -> Dict[str, Any]:
        recent_episodes = episode_store.get_recent_episodes(user_id=user_id, limit=3, tenant=tenant)
        current_facts = fact_store.get_current_facts(subject=subject, tenant=tenant)

        summary_parts = []
        if recent_episodes:
            summary_parts.append("Previous session context: " + "; ".join([e["summary"] for e in recent_episodes]))
        if current_facts:
            summary_parts.append("Current facts: " + "; ".join([f["text"] for f in current_facts]))

        return {
            "has_context": bool(summary_parts),
            "context_prompt": " | ".join(summary_parts),
            "episodes": recent_episodes,
            "facts": current_facts
        }

historian_agent = HistorianAgent()
