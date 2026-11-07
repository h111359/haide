# BL-0002 decisions

- User request: realize BL-0002. User explicitly allowed clearly labelled estimates from configured rates, otherwise unavailable.
- Keep usage operations in core, independent of any installed role or network billing service.
- Host explicitly assigns session identity and position ranges; do not scan unrelated sessions or infer complete account coverage.
- Keep immutable source bindings and last-good checkpoints; reject rewritten sources, edited report/checkpoint inconsistencies and unsafe targets.
- Distinguish measured tokens, caller-reported charges and configured-rate equivalents. Require an explicit currency and money-per-credit value for money estimates. The unanswered optional conversion question defaults to unavailable under the user's chosen policy.
- Refresh before closure; never count future/unsaved usage or claim an invoice. Usage artifacts are excluded from stable recording-proof hashes because closure refresh modifies them.
- Leave backlog acceptance pending and Activity active. No commit, close or push was requested for this task.


Revision provenance: source: User BL-0002 implementation request and estimate-policy answer; observed test evidence; reason: Record completed implementation and checks without implying acceptance; reason: Preserve user policy and implementation boundaries; recorded 2026-11-06T17:49:31Z.

## EUR list-price clarification (2026-11-06T21:47:50Z)

User selected EUR and requested valuation according to list price. This supersedes asking the user to choose an arbitrary value. Use the verified applicable official EUR credit purchase list price when available, retaining price source and date. The official pricing page checked today establishes token-to-credit rates but no applicable EUR per-credit purchase price; it says purchase prices vary by plan/agreement. Therefore leave money unavailable. Do not substitute API prices, monthly subscription fees or USD/EUR parity. Evidence: files/BL-0002-money-policy.json.


Revision provenance: source: User EUR answer and list-price clarification; official OpenAI pricing page; reason: Preserve clarified monetary estimation policy; reason: Record user-selected currency and list-price basis without inventing an unavailable price; recorded 2026-11-06T21:47:50Z.

## Superseding scope change: tokens and credits only (2026-11-07T05:13:06Z)

User instructed: “OK, disregard money estimate - put the token and credits only”. Removed monetary report fields, estimates and currency/value-per-credit configuration. Tokens, caller-reported credits and configured-rate credit equivalents remain. Earlier EUR/list-price policy is superseded; historical records remain audit evidence only. Format 2 is token/credit-only; format-1 checkpoints with null money values remain readable and update to format 2. Non-null legacy monetary values require explicit preservation. Verification: all 54 runtime tests passed, including 19 usage tests covering omission, rejected monetary configuration and null legacy compatibility. Earlier unaffected suites had 168 passes and two Windows-specific skips; combined matrix is 224 tests, 222 passed and two skipped. No commit or Activity closure.


Revision provenance: source: User 2026-11-07 tokens-and-credits-only instruction; reason: Remove superseded monetary estimation scope; reason: Record superseding user scope and verified token/credit-only implementation; recorded 2026-11-07T05:13:06Z.
