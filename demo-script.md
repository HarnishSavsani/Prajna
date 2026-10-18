# Prajna (प्रज्ञा) Demo Video Script & Shot-List

> **Target Duration**: 2 minutes 50 seconds (Hard Cap: 3:00)  
> **Resolution**: 1080p 60fps / 16:9  
> **Speaker Pace**: Clear, punchy, confident, technical.  
> **Theme**: Calm Indian-rooted teal brand, proof-of-work "Why?" paths, permissions-as-edges, and the FalkorDB removal test.

---

## Scene Overview & Timing Breakdown

| Scene | Time Window | Scene Name | Primary Visual | Key Audio Takeaway |
|---|---|---|---|---|
| **Scene 1** | `0:00 - 0:25` (25s) | **The Hook** | Side-by-side: Flat Search vs Work Graph | *"AI search fails when the answer lives in the connections between tools."* |
| **Scene 2** | `0:25 - 0:55` (30s) | **Who-Knows & Why? Path** | UI chat + "Why?" drawer + PageRank | *"Alice Chen isn't just mentioned in docs; she has 0.80 PageRank over real commits."* |
| **Scene 3** | `0:55 - 1:25` (30s) | **Entity Resolution & Blast Radius** | Ambiguous prompt "Browser" → DAG traversal | *"Resolves ambiguous entities across products and calculates multi-hop blast radius."* |
| **Scene 4** | `1:25 - 1:55` (30s) | **Permission Security (Intern vs Lead)** | Persona toggle + Saffron banner + Mascot eye closes | *"Zero leaks. Filtered in Cypher before data touches the LLM."* |
| **Scene 5** | `1:55 - 2:25` (30s) | **Draft Action & 'Continue Yesterday'** | Close-the-loop draft + cross-session memory recall | *"Memory in FalkorDB nodes; versioned optimistic concurrency with 0 double-claims."* |
| **Outro** | `2:25 - 2:50` (25s) | **The Removal Test & Benchmark Proof** | `docker stop prajna-falkordb` + verify.py table | *"FalkorDB is the engine, not decoration. 100% grounding, 0 leaks, 2.2ms latency."* |

---

## Detailed Storyboard & Narration

### Scene 1: The Hook (`0:00 - 0:25` | 25s)
- **Visual**:
  - `0:00 - 0:10`: Split screen illustration or animated slide. On the left: Standard AI document search returning a wall of disconnected Slack links and outdated READMEs. On the right: Prajna’s clean teal UI with the FalkorDB graph topology underneath.
  - `0:10 - 0:25`: Pan into the live Prajna interface (`http://localhost:3000`). Show clean typography, the Prajna wisdom logo, and the starter query cards.
- **Narration (Voiceover)**:
  > *"When an author leaves a software team, answering 'who knows this service?' or 'what breaks if we change this?' isn't in a single document. It lives in the relationships between people, PRs, issues, and architecture decisions.  
  > Meet Prajna — the open-source, graph-native AI teammate built on FalkorDB."*

---

### Scene 2: Who-Knows with Traceable Graph Path (`0:25 - 0:55` | 30s)
- **Visual**:
  - Type query into Prajna chat bar:  
    `"Who knows the payments-service and its auth module?"`
  - Press enter. Stream begins immediately (< 200ms TTFT).
  - Prajna streams reasoning tokens, executes tool step `who_knows`, and returns:  
    **Alice Chen (Score: 0.80)** and **Bob Taylor (Score: 0.80)**.
  - Click on citation / "Why?" evidence path button. A slide-out panel reveals the 4-hop graph proof:  
    `Alice Chen` → `AUTHORED` → `PR#102 (Fix payment gateway timeout)` → `payments-service`.
- **Narration (Voiceover)**:
  > *"We ask who knows the payments service. Instead of hallucinating or scanning flat text, Prajna executes a PageRank algorithm in Cypher across commit authors and code reviewers.  
  > Click 'Why?' and every answer gives you verifiable proof: a 4-hop graph path straight from code to author in 2.2 milliseconds."*

---

### Scene 3: Entity Resolution & Blast Radius (`0:55 - 1:25` | 30s)
- **Visual**:
  - Ask conversational, ambiguous query:  
    `"What's the status of Browser?"`
  - Show the Router agent resolving "Browser" specifically to `product:falkordb_browser` rather than generic web browsing.
  - Next query: `"What is the blast radius of modifying payments-service?"`
  - Result displays upstream and downstream affected services (`checkout-service`, `auth-service`, `notifications-service`, `audit-service`) ranked by DAG betweenness centrality.
- **Narration (Voiceover)**:
  > *"Prajna handles real engineering ambiguity. When we ask about 'Browser', entity resolution binds directly to the FalkorDB Browser product node.  
  > Asking for the blast radius executes multi-hop DAG traversal across CALLS and DEPENDS_ON edges, calculating betweenness centrality to show exactly what breaks downstream."*

---

### Scene 4: Pre-LLM Permission Security (`1:25 - 1:55` | 30s)
- **Visual**:
  - Top bar: Show user persona toggle set to **Security Lead (Admin)**. Query confidential services or Eve Secret. Full authorized data renders.
  - Switch persona dropdown to **Intern (Restricted User)**.
  - Submit the identical query: `"Tell me about the payments secret gateway and Eve's project."`
  - Prajna returns the **saffron-bordered restricted state banner**:  
    `🔒 You don't have access to that.`
  - The Prajna mascot eye transitions to its closed state. Zero sensitive titles, paths, or citations are emitted in the SSE stream.
- **Narration (Voiceover)**:
  > *"Security can't be a prompt prompt-hack. In Prajna, permissions are enforced as graph edges via `scoped_match()` before the LLM is ever called.  
  > Querying as an intern, the mascot's eye closes, the saffron restricted banner activates, and Eve's confidential data is mathematically pruned at the database level. Target: 0 leaks. Measured: 0 leaks."*

---

### Scene 5: Draft Action & Cross-Session Memory (`1:55 - 2:25` | 30s)
- **Visual**:
  - Query: `"Draft a close-the-loop update for the checkout timeout issue fixed in Release v1.2.0."`
  - Show Prajna tracing `Release` → `PR` → `Issue` → `Ticket` → `Person` to generate draft emails for Acme Corp and Globex Ops (clearly tagged as **DRAFT ONLY — NEVER SENT**).
  - Open a brand-new chat session. Ask:  
    `"Continue where we left off yesterday regarding checkout latency."`
  - Historian agent recalls `Episode` and `Fact` nodes from FalkorDB, synthesizing yesterday's discussion without repeating context.
  - Show multi-agent `Task` coordination node claiming task with optimistic concurrency: 0 double-claims.
- **Narration (Voiceover)**:
  > *"Prajna closes the loop by tracing fixed bugs back to complaining customers and drafting notifications without human toil.  
  > And memory isn't ephemeral RAM. Personal and team facts are stored with temporal validity in FalkorDB. Starting a new session, Prajna recalls past context while optimistic concurrency guarantees zero double-claims across autonomous agents."*

---

### Outro: The Removal Test & Proof (`2:25 - 2:50` | 25s)
- **Visual**:
  - Split screen: Terminal on left, Browser on right.
  - Run terminal command:  
    ```bash
    docker stop prajna-falkordb
    ```
  - Click refresh / submit query in Prajna UI. The app immediately stops: clear error indicating graph unreachable.
  - Restart FalkorDB:  
    ```bash
    docker start prajna-falkordb
    ```
  - Cut to terminal running `python verify.py` displaying the clean benchmark console table:  
    - Permission Leaks: 0  
    - Grounding: 100.0%  
    - Entity Resolution: 96.7%  
    - Latency: 2.2 ms  
  - Final splash card with GitHub repo URL and Track 01, 02, 03 badges.
- **Narration (Voiceover)**:
  > *"Hackathon rule 3: FalkorDB cannot be decoration. Watch what happens when we stop FalkorDB: the app instantly halts. It's not a cache — it is the intelligence engine.  
  > 100% grounding, sub-3ms graph latency, 0 leaks. Everything you saw is reproduced by our autonomous verification suite.  
  > Prajna is open source and ready to run. Thank you."*
