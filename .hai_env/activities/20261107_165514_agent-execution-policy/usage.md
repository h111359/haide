# Activity usage

Activity: `ef45d9ae-52ff-47e1-8a48-00f8b55b421f`

Updated: 2026-11-07T16:55:14Z

Coverage: **observed** for explicitly assigned source ranges only.

This is the latest observed snapshot, not an invoice. Unregistered sessions and future or unsaved usage are not included.

## Tokens

| Metric | Observed value |
| --- | --- |
| input_tokens | 3269871 |
| cached_input_tokens | 3238912 |
| output_tokens | 13080 |
| reasoning_output_tokens | 2056 |
| total_tokens | 3282951 |

Cached input is included in input; reasoning is included in output. Total is input plus output, without adding those subsets again.

Partial/stale coverage shows last-known token values; it does not establish complete current usage.

## Credits

| Kind | Value |
| --- | --- |
| Caller-reported credits | Unavailable |
| Estimated credit equivalent | 12.91523 |

Estimates use the supplied rate snapshot; they are not actual debited credits or subscription charges. Quota percentages and remaining credit balances are never spend.

Rate source: https://learn.chatgpt.com/docs/pricing — Standard credit-rate equivalent, not actual subscription spend; checked 2026-11-06

Rate captured: 2026-11-06T17:42:28Z

| Model | Input credits / 1M | Cached input credits / 1M | Output credits / 1M |
| --- | --- | --- | --- |
| gpt-6.1-sol | 50 | 2.5 | 250 |

## Sources

| Session | Assigned positions | Latest token position | Status |
| --- | --- | --- | --- |
| 01a1ad56-2eaf-7821-92a7-3bdc5f4f6bb9 | 1831..live | 1978 | current |

Source cutoffs, last-good observations and provenance are retained in `usage.json`. Updates before closure include only usage already available at that time.
