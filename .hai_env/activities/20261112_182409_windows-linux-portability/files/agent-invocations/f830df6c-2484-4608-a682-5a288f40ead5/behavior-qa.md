# Independent behavior QA

Result: PASS for the inspected native Windows implementation. No product defects found in final executed scenarios.

- Runtime: Windows (`win32` / `nt`), Python 3.14.7.
- Public CLI: 61 successful expected-result checks across two independent isolated fixture workspaces (30 event_msg, 31 response_item).
- Native safety: 18 passing probes, no skips.
- Fixtures and subprocess TMP/TEMP/TMPDIR remain inside this invocation.

## Exercised acceptance criteria

Public CLI initialization/configuration and startup execution_context; Activity create/discover/show with canonical paths; step/log updates; decisions.md revisions preserving the previous artifact bytes including provenance; exact Unicode chat round-trip; usage update/read; invocation allocation; source discovery, explicit response_item recovery from default event_msg mismatch, binding, synchronization and verification for both representations; package installation and canonical difference paths; duplicate installation and traversal/native/absolute source rejection; enabled-recording closure; archived supplement, chat, usage and recording verification; fresh Activity identity and chat isolation. Fixture workspace names contain Unicode and spaces.

Safety probes reject traversal, absolute/drive paths, backslash input, empty/dot components, device names, trailing dots/spaces, colon and invalid wildcard characters. Actual Windows junctions are rejected at the junction and existing/nonexistent descendants. Native archival rename collision retains source and destination contents without replacement.

## Evidence

- `cli-results.json`: all CLI envelopes/exit codes, fixture paths, runtime details and reviewed source hashes.
- `safety-results.json`: each negative/native check and actual error.
- `cli_behavior.py`, `native_safety.py`: independently authored reproduction harnesses.

The first exploratory CLI run stopped because the QA harness assumed artifact text did not include automatically appended revision provenance. Inspection confirmed the product behaved as designed; the harness was corrected to compare revision bytes against the actual previous artifact. The final complete 61-operation run passed.

## Limits

Native Linux and Python 3.11 execution were not available to this reviewer. CI configuration is not evidence of a completed Linux run. These tests do not authenticate session provenance or billing, prove all filesystem race protection, or certify every optional agent script. Usage source attribution for this QA host is unavailable. No live Activity lifecycle or transcript mutations, product changes, or subordinate agents by this reviewer. Only runtime chat coordination was posted to the live Activity.
