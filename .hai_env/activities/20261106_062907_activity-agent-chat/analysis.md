# BL-0001 implementation evidence

Implemented Activity-local coordination as runtime read/append operations, not
another optional agent. chat.jsonl is lazy, identity-bound and retained on archive.
Only chat-post applies changes, under the existing environment lock, using a
single append syscall and exact-prefix readback. Existing invalid history blocks
posting; partial writes are reported without rollback/retry. Read pages are bounded
but the whole existing history is validated. Chat uses independently declared
format 1 and does not require a state migration.

Updated core Activity/agent/startup instructions with participation and ownership
boundaries. Canonical artifacts, exact chronicles and lifecycle ownership remain
separate. Startup checks optional chat file type/access, not message contents.
README identifies this feature as unreleased beyond the prepared 0.3.0 ZIP.

Verification on Linux/Python 3.12.3: 15 new chat tests passed, including CLI behavior,
multiple fixture authors, exact Unicode/whitespace, append preservation, lock
contention, short writes/fsync failures, unsafe links, malformed history, archival
and fresh Activity isolation. Full core checks ran 191 tests: 189 passed and two
Windows-only tests skipped. A real host-coordinator message was previewed, posted
and read back with exact text; no other agent participation was invented.

Limits: author/provenance are caller supplied; direct same-account filesystem
access can bypass the supported append-only API. No OS security boundary,
cryptographic tamper proofing, notification service or background agent execution
is claimed. Windows/macOS execution unverified. BL-0001 remains pending for user
acceptance; this Activity remains open and no commit was requested.

Evidence: files/BL-0001-test-results.json and
files/BL-0001-live-chat-verification.json.


Revision provenance: source: User: Now work on BL-0001; actual implementation/test results; reason: Record completed implementation and precise verification limits; reason: Actual implementation and acceptance evidence for BL-0001; recorded 2026-11-06T05:45:47Z.
