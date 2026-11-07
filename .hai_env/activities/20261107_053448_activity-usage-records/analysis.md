# BL-0002 implementation and verification

Implemented source-bounded Activity usage snapshots in core runtime. On-demand usage-update and automatic pre-closure refresh write usage.md plus usage.json. usage-read supports current and archived snapshots without reopening saved sources. Closure with no sources produces explicit unavailable values; invalid retained state or persistence failure blocks closure before lifecycle writes. Partial output is retained and reported.

The explicit root session 01a1ad56-2eaf-7821-92a7-3bdc5f4f6bb9 is assigned from physical position 1287 (the BL-0002 user prompt). Earlier session work is excluded. No other session was invoked or discovered for this task. Coverage applies to assigned ranges only, not all account usage. Saved cumulative counters are differenced with monotonicity, prefix-integrity and identity checks; repeated snapshots do not double count. Missing sources retain stale last-good observations rather than fabricated zero.

Reported charges are caller-attested and cutoff-bound. Estimates use explicit decimal-string model rates, source and capture time. The user authorized labelled estimates or unavailable. The live report uses the checked official Standard credit-rate equivalent for the observed model, not an actual subscription charge. No money conversion was supplied, so monetary estimates and actual charges are unavailable. Quota balances never become spend.

Verification: 53 runtime tests passed (18 usage-specific); startup 66 run with 64 passed and two Windows-only skips; activities 16, agents 75 and configuration 13 passed. Total 223 run, 221 passed, two skipped on Linux. Evidence: files/BL-0002-test-results.json and files/BL-0002-final-runtime-tests.json. Live idempotent refresh/readback evidence: files/BL-0002-live-verification.json. git diff --check and core startup passed. No Windows/macOS execution or authenticated billing integration claimed.


Revision provenance: source: User BL-0002 implementation request and estimate-policy answer; observed test evidence; reason: Record completed implementation and checks without implying acceptance; reason: Record actual implementation, verification and source coverage limits; recorded 2026-11-06T17:49:31Z.

## Superseding scope change: tokens and credits only (2026-11-07T05:13:06Z)

User instructed: “OK, disregard money estimate - put the token and credits only”. Removed monetary report fields, estimates and currency/value-per-credit configuration. Tokens, caller-reported credits and configured-rate credit equivalents remain. Earlier EUR/list-price policy is superseded; historical records remain audit evidence only. Format 2 is token/credit-only; format-1 checkpoints with null money values remain readable and update to format 2. Non-null legacy monetary values require explicit preservation. Verification: all 54 runtime tests passed, including 19 usage tests covering omission, rejected monetary configuration and null legacy compatibility. Earlier unaffected suites had 168 passes and two Windows-specific skips; combined matrix is 224 tests, 222 passed and two skipped. No commit or Activity closure.


Revision provenance: source: User 2026-11-07 tokens-and-credits-only instruction; reason: Remove superseded monetary estimation scope; reason: Record superseding user scope and verified token/credit-only implementation; recorded 2026-11-07T05:13:06Z.
