# Prajna — Testing & GSD Workflow (read before finishing any task)

> Rule for every AI session: **nothing is "done" until a test proves it and the work is committed.**
> "Green test → commit" is one unit of work. No green test → not done.

---

## 1. The GSD loop (Git Shit Done) — run after EVERY completed unit

A "unit" = one file/function/tool from a Phase step, not a whole phase.

1. **Build** the unit (follow Rules.md).
2. **Write/extend its test** (section 3) — the test comes with the code, not later.
3. **Run the test.** If red, fix and repeat. Never commit red.
4. **Run the quick smoke** (`make smoke`, section 4) so you didn't break earlier phases.
5. **Commit** with a conventional message (section 5). Auto-commit is allowed here.
6. **Update `vibe-coding/Memory.md`** (tick the Phase checkbox + one Session-Log line).
7. **Do NOT push automatically.** Push only when the human says "push" (section 6).

If any step 3–4 fails, stop and report; do not proceed to the next unit.

## 2. Testing philosophy (hackathon-calibrated)
- **Must be tested:** the permission prefix (`scoped_match`), every MCP tool query, `claim_task` concurrency, ingestion idempotency, the SSE packet contract, and anything `verify.py` scores.
- **May stay untested:** UI components, rebrand/CSS, one-off scripts.
- Prefer **fast, deterministic** tests over broad ones. A tool test that asserts the right nodes come back beats a mocked unit test.
- Tests use the **real FalkorDB** (from compose) against a **small seeded test graph**, not mocks — graph behaviour is the product.
- Every test must be **re-runnable**: it seeds what it needs and cleans up (or uses a throwaway `tenant_test` graph).

## 3. What test to write for each unit
| Unit type | Test to write | Pass assertion |
|---|---|---|
| `falkor_client` / `schema` | connect + create 18 indexes on `tenant_test` | all indexes exist; no error |
| `github_loader` | load a tiny fixture repo twice | counts non-zero; second run adds 0 (idempotent) |
| `synthetic_overlay` / `identity` | load overlay; stitch a known dual-identity person | exactly one `Person` node for that person |
| `permissions.scoped_match` | query as allowed vs restricted user | restricted node absent from results |
| MCP tool (e.g. `who_knows`) | run on seeded graph | returns expected ranked ids; latency printed |
| `claim_task` | two concurrent claims | exactly one succeeds; 0 double-claims |
| SSE endpoint | send a message, read the stream | packet sequence valid; ends with `stop` |
| memory | write then recall in a new "session" | prior fact/episode returned; outdated fact shows superseded |
| tenancy | query tenant A for a B node | returns nothing; `GRAPH.LIST` shows both |

## 4. Test commands (Makefile targets to create in `prajna/`)
```
make test        # full pytest suite (needs FalkorDB up)
make test-unit   # fast tests only (permission prefix, claim_task, packet shape)
make smoke       # 30-sec sanity: boot routes 200, one who_knows answer, SSE ends in stop
make verify      # run verify.py → JSON + console table (the demo numbers)
make up / down   # docker compose -f docker-compose.prajna.yml up/down
```
`make smoke` after every unit; `make verify` at the end of each phase.

## 5. Commit conventions (what GSD commits)
- `feat(phase1): github_loader with idempotent MERGE`
- `test(phase1): permission prefix hides restricted docs`
- `fix(phase1): stitch persons by verified email first`
- `docs: update Memory.md after who_knows`
- `chore: ...`
One unit = one commit. Keep the tree green at every commit.

## 6. Push rules (IMPORTANT — protects your one submission repo)
- **Auto-commit: yes. Auto-push: no.** The AI commits locally; the human pushes.
- Push only on an explicit "push" instruction, and only after `make verify` is green.
- Never force-push `main`. Never rewrite history (it must show real event dates, rule 8).
- Never commit `.env`, data dumps, tokens, or `node_modules`.
- First push: make sure the repo is created fresh during the event (no pre-event commits).

## 7. "Definition of done" for a unit (all true)
- [ ] Code follows Rules.md (FalkorDB-only, Cypher reasoning, permission prefix used)
- [ ] Its test is written and **green**
- [ ] `make smoke` still green (didn't break earlier phases)
- [ ] Committed with a conventional message
- [ ] `Memory.md` updated
- [ ] Not pushed (unless human said so)

## 8. "Definition of done" for a phase
- [ ] All units done per section 7
- [ ] All Phase checkboxes in `Phases.md` ticked
- [ ] `make verify` green; numbers recorded in `Memory.md`
- [ ] Exit criteria in `Phases.md` for that phase met (human-confirmed in the UI where relevant)

## 9. AI self-test prompt (paste when asking the AI to test its own work)
> After implementing <unit>, follow TESTING.md: write its test (section 3), run `make test-unit` and `make smoke`, fix until green, commit with a conventional message, update `Memory.md`. Do NOT push. Report what you tested, the result, and the commit hash. If anything is red, stop and show me the failure.