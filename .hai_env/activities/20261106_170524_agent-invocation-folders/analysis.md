# BL-0010 — Implementation and verification

User authorized implementation after the relevant-agent reviews and consolidated
plan. The recommended defaults were applied: a new spawn gets a fresh folder,
a same-live-instance follow-up retains its folder, and material remains with its
Activity without automatic cleanup.

## Implemented behavior

Added activity invocation-allocate to the core runtime. It validates the sole
current stable Activity ID, supplied agent and provenance, derives a UUID-based
folder under files/agent-invocations/, and creates it and invocation.json exclusively
under the shared runtime lock. Preview reserves nothing. Applied success returns
existing workspace-relative/Activity-relative paths and attribution metadata.
Changed identity, collision, unsafe parents and metadata/readback errors cannot
return dispatchable success; partial creations are preserved and reported.

Shared startup/agent/Activity instructions now require allocation before each new
spawn, initial assignment handoff, binding the actual returned host handle, and
verified writer quiescence before host closure. Allocation is not launch evidence.
No runtime spawning engine, global registry, core state migration, package/config
change, cleanup service or OS security boundary was introduced.

## Actual verification

All 14 new allocation tests passed. Core regression suites ran 205 tests: 203
passed and two Windows-only tests skipped, Linux/Python 3.12.3. Fixture coverage
includes preview/apply, same-role uniqueness, collisions, strict requests, unsafe
parents, changed state, partial file/directory failures, lock contention, closure
serialization, configured stores, CLI and archive/new-Activity separation.
An initial fixture assertion counted both allocator and runtime-lock UUID calls;
that test assertion was corrected before the final passing runs.

Three real quality-assurance probes used an isolated verification workspace nested
in this Activity's ignored test-work directory. A/B were overlapping invocations
of the same agent with different applied allocations supplied before spawn. Both
validated manifests and wrote independent files. A follow-up to A retained its
folder and original bytes. Host observed both running and withheld closure.
After actual completed handoffs and no-background-writer reports, the host archived
the test Activity and verified every recorded invocation byte hash.

Probe C received a new allocation in a second test Activity after active-path reuse;
old-ID allocation was rejected and prior archived bytes were preserved. C finished
before that test Activity was closed. A controlled allocated-but-not-dispatched
case retained its folder and was never described as an actual launched agent.

The final independent QA invocation /root/qa_bl0010_final was allocated in THIS
Activity before spawn: invocation fd8f3a49-8989-469d-a14a-aa76ac8b1670. Its own review
and report are in that working folder. It independently verified ten recorded
archive hashes and found no high/medium issues; it reviewed prior suite results
without rerunning them. Final handoff reports no background writers and finished
writing. Both role identity and host handle are attributable actual values.

## Evidence and limits

- files/BL-0010-test-results.json — commands and actual suite results.
- files/BL-0010-host-verification.json — real host handles, reports, identity/folder
  checks, follow-up, blocked closure while running, archival hashes and AC1–5 map.
- files/agent-invocations/fd8f3a49-8989-469d-a14a-aa76ac8b1670/review.md and report.json —
  independent final QA and real product-Activity allocation use.

Product git diff --check and 44 local documentation targets passed. No real
indeterminate host launch was induced; controlled no-dispatch and injected storage
failure evidence are labelled. Host writer coordination is not enforcement of
external process lifetime by direct runtime close calls or OS isolation. Windows
and macOS execution remain unverified. Live installed optional agents/settings
are unchanged. This product Activity remains open; BL-0010 remains pending user
acceptance and no commit or publication was requested/performed.


Revision provenance: source: User: implement; actual runtime tests, host probes and final QA result; reason: Complete authorized implementation and record reviewable evidence; reason: Actual implementation, fixture/real-host results and independent final QA; recorded 2026-11-06T10:20:30Z.
