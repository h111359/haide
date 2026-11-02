# Read-only Codex source adapter

`read_codex_source.py` requires Python 3.11+ and the standard library. Verify an
absolute interpreter under the core tooling convention before execution. Pass
only the explicitly authorized canonical source; no session discovery occurs.

From an installed workspace package:

```text
<absolute-python-executable> -B .hai_env/agents/codex-chronicle-manager/scripts/read_codex_source.py /explicit/session.jsonl --representation event_msg --expected-session supplied-session-id
<absolute-python-executable> -B .hai_env/agents/codex-chronicle-manager/scripts/test_read_codex_source.py
```

The [source convention](../conventions/codex-source_conv.md) documents the supported
conservative JSONL subset and representation choice. Older/future schemas, ambiguous
assistant phases, missing metadata, malformed/truncated records or changed sources
return `ok: false` with explicit issues. Select one representation and retain it;
never merge event/response duplicates. Blank records and duplicate JSON keys fail.
Repeated resume metadata is accepted only for the exact same original session ID
and start timestamp; changing outer resume time or nonidentity metadata does not
renumber occurrences. Conflicting original identity/start still blocks reading.

The API is `read_source(path, representation, expected_session=None)`. JSON output
has `ok`, source identity/start, `representation`, `durable_path`, `source_sha256`,
`messages` and `issues`. Each normalized message has exact decoded `text`, `role`,
actual `timestamp`, `source_session_id`, stable physical `source_position` and an
optional original `message_id`. Physical positions are zero-based JSONL lines,
including excluded records. Repeated identical messages retain different positions.
The adapter has no writes, side effects, downloads or external dependencies. Exit 0
means the selected source subset parsed completely, 1 means unavailable/incomplete
source and 2 is CLI argument misuse. Returned partial messages never prove complete
coverage. Paths outside the workspace require the caller's supplied source authority;
acceptance of a path by this parser is not permission to read it.

This tool neither scans sources nor creates or advances transcripts/checkpoints.
It does not establish Activity attribution, enabled intervals, retained-source
completeness or coverage; owner procedures perform those checks and compare exact
existing segments. A trailing incomplete source record blocks progress past that
boundary rather than being silently discarded. Tests use disposable textual
fixtures, not a user's actual sessions.

The source convention permits an explicitly assigned immutable exact-byte prefix
snapshot for a live source. The reader treats that canonical file as supplied and
preserves its original physical positions; it does not create the snapshot or
prove its original-source provenance. Chronicle separately verifies the original
prefix and absence of later eligible exchanges before claiming closure freshness.
Excluded tool records appended to the live original do not by themselves change
the immutable prefix fingerprint; changed original text or new eligible exchanges
still invalidate stale closure evidence.
