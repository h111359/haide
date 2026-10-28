# Prepare 0.2.0 and commit

Recorded 2026-10-28T07:23:19Z from leader’s supplied coordination plan after the user selected 0.2.0.

1. Prepare consistent 0.2.0 source manifest and release documentation, accounting for the verified v0.1.0 baseline and Activity transition. Release owner records candidate/check evidence in results/release-preparation.md.
2. Finish applicable source checks and ensure the intended source set is ready. Keep package output under ignored dist; preserve the predecessor’s closed identity and source history.
3. Have leader obtain a fresh source-backed chronicle refresh for this specific commit operation, including proper Activity boundaries and delayed predecessor catch-up as applicable.
4. Git-manager performs the authorized source commit after the fresh gate, then exports the exact committed source and reports the commit identity.
5. Release owner builds the local ZIP from that exact export, verifies package contents and source/manifest consistency, and records artifact/checksum evidence.
6. Record supplied final evidence and remaining limitations without closing this Activity automatically. Do not push, publish or create tags.

Open dependencies: candidate preparation, fresh pre-commit gate, source commit/export and exact-package verification. The version is settled; these execution results remain pending. Activity-manager freezes its authored records after this update until leader requests further changes, avoiding competing writes during commit preparation.
