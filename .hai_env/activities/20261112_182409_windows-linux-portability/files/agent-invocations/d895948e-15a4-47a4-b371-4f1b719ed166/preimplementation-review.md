# Independent implementation QA checklist

Validated supplied invocation manifest and Activity identity. Mandatory instructions are readable and empty. Followed installed QA role; no product edits.

Entry runtime chat-read was attempted but blocked by native backslash path in activities.py; retry after fix.

Confirmed additional blocker: chronicles.py:263 uses ZoneInfo("Europe/Sofia"). A native probe with the supplied Python 3.14.7 fails with ZoneInfoNotFoundError because tzdata is absent. Preserve existing segments; choose/document portable new-segment naming or provide explicit timezone data. Reported to coordinator.

Final review checklist:
- All workspace-relative output and input handoffs canonical; native absolute external paths retained separately.
- Discovery, updates, artifact revisions, show/chat/usage reads, supplements, overlap checks, snapshots and partial changed_files.
- Junction/reparse-point and hard-link rejection; traversal, reserved device names, trailing dots/spaces, drive/UNC/ADS and invalid Windows characters.
- Case-insensitive protected-path overlap and aliases, preserving valid Linux case sensitivity.
- Preview no writes, locks and fingerprints retained, no-overwrite rename collision safety.
- Source representation remains explicit, source identity/ranges unchanged.
- Native CLI workflows and lifecycle recording closure; test contexts isolate temp writes inside invocation or Activity.
- CI genuinely runs Windows/Linux on minimum/current Python, reports capability skips; no claim of unobserved Linux success.
- Startup runtime information distinguishes OS/Python from shell, recording representation and feature readiness.

Usage-source metadata is not available to this reviewer. Awaiting implementation-ready signal before final diff review.
