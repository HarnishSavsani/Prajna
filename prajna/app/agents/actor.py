from typing import Any, Dict, List, Tuple
from prajna.app.memory.sessions import session_store

class ActorAgent:
    """
    Synthesizes retrieved graph data into final response, computes citations,
    and records Answer node with USED evidence edges into FalkorDB.
    """
    def synthesize_and_record(
        self,
        query: str,
        tool_name: str,
        retrieval: Dict[str, Any],
        session_id: str,
        tenant: str = "kirana"
    ) -> Tuple[str, List[Dict[str, Any]]]:
        raw_rows = retrieval.get("raw_rows", [])
        params = retrieval.get("params", {})
        target = params.get("target", "")

        citations = []
        evidence_ids = []

        if tool_name == "who_knows":
            if not raw_rows:
                answer = f"I examined the organization graph, but found no recorded PR authors or reviewers for `{target}`."
            else:
                top = raw_rows[0]
                name = top[1]
                score = top[2]
                authored = top[3]
                reviewed = top[4]
                answer = (
                    f"Based on code contribution and review centrality in our organization graph, "
                    f"**{name}** knows `{target}` best (expertise score: {score}). "
                    f"They have authored {authored} PRs and reviewed {reviewed} PRs in relevant modules."
                )
                citations.append({"citation_number": 1, "document_id": f"person:{top[0]}"})
                evidence_ids.append(top[0])

        elif tool_name == "blast_radius":
            if not raw_rows:
                answer = f"No downstream service dependencies found for `{target}`."
            else:
                dependents = [r[1] for r in raw_rows]
                answer = (
                    f"**Blast Radius for `{target}`**:\n"
                    f"Changing this service affects {len(dependents)} downstream services: "
                    f"{', '.join(dependents)}. Multi-hop dependencies were traced up to 4 hops in FalkorDB."
                )
                for idx, r in enumerate(raw_rows[:3], start=1):
                    citations.append({"citation_number": idx, "document_id": f"service:{r[0]}"})
                    evidence_ids.append(r[0])

        elif tool_name == "bus_factor":
            if not raw_rows:
                answer = f"No module contribution data found for target `{target}`."
            else:
                risks = [r for r in raw_rows if r[4]] # single point of failure
                if risks:
                    risky_names = [f"**{r[1]}** (maintainer: {', '.join(r[3])})" for r in risks]
                    answer = f"⚠️ **Bus Factor Alert**: {len(risks)} module(s) have only 1 contributor:\n- " + "\n- ".join(risky_names)
                else:
                    answer = f"All surveyed modules under `{target}` have a healthy bus factor with multiple active contributors."
                citations.append({"citation_number": 1, "document_id": "bus-factor-report"})

        elif tool_name == "impact_ranking":
            if not raw_rows:
                answer = "No customer tickets currently linked to product features."
            else:
                lines = []
                for idx, r in enumerate(raw_rows, start=1):
                    lines.append(f"{idx}. **{r[1]}**: {r[2]} customer complaint(s) ({', '.join(r[3])})")
                    citations.append({"citation_number": idx, "document_id": f"feature:{r[0]}"})
                    evidence_ids.append(r[0])
                answer = "Customer Complaint Impact Ranking:\n" + "\n".join(lines)

        elif tool_name == "decision_trace":
            if not raw_rows:
                answer = f"No Architectural Decision Record found matching `{target}`."
            else:
                d = raw_rows[0]
                answer = f"**Decision `{d[0]}`**: {d[1]}\nStatus: {d[3] or 'Active'}\nEvidence: {', '.join(d[4]) or 'None'}"
                citations.append({"citation_number": 1, "document_id": f"decision:{d[0]}"})
                evidence_ids.append(d[0])

        elif tool_name == "draft_close_the_loop":
            if not raw_rows:
                answer = f"No resolved issue found matching `{target}`."
            else:
                i = raw_rows[0]
                recipients = i[4] or ["Affected Customers"]
                answer = (
                    f"### [DRAFT] Customer Update Notification\n"
                    f"**To:** {', '.join(recipients)}\n"
                    f"**Subject:** Fix Shipped: {i[1]}\n\n"
                    f"We are pleased to inform you that the issue *'{i[1]}'* has been fixed in release `{i[2] or 'v1.4.0'}`. "
                    f"Thank you for your patience while we resolved this."
                )
                citations.append({"citation_number": 1, "document_id": f"draft-notification:{i[0]}"})
                evidence_ids.append(i[0])

        else:
            answer = f"Query executed with {tool_name}. Retrieved {len(raw_rows)} records from FalkorDB."

        # Persist Answer in FalkorDB
        cypher_used = f"Tool: {tool_name} | Params: {params}"
        session_store.record_turn(
            session_id=session_id,
            query=query,
            answer_text=answer,
            cypher_used=cypher_used,
            evidence_ids=evidence_ids,
            tenant=tenant
        )

        return answer, citations

actor_agent = ActorAgent()
