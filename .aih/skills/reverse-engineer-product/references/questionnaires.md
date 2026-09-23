# Questionnaires and returned answers

The authoritative questionnaire is UTF-8 Markdown. A question begins:

```markdown
## Q-ACCESS | revision=1 | respondent=Requestor | kind=single | blocker=true | category=requirement
Question: Which employees should be able to see a submitted request?
Explanation: We need to know who may read requests after they are sent.
Why we ask: Your answer defines whose access must pass the acceptance checks.
How to answer: Select one option or describe a different rule in Answer.
Example: Illustration only: a team might limit access to the submitting employee and their manager.
Default: No default; the required answer remains unresolved.
- [ ] The submitting employee only
- [ ] The employee and their manager
Answer:
Comments:
```

Stable IDs and integer revisions persist. Respondent is `Framework user` or `Requestor`; kind is `text`, `single`, or `multiple`. A consequential blocker is distinct from optional questions with documented defaults. Every question has a free-text answer. Recommendations are labeled with rationale and start unchecked. Invalid mutually exclusive choices, malformed content or text contradicting a choice require explicit resolution. Catalogs summarize/link this one answer source.

The semantic writer provides understandable question, situation/terms explanation, why the answer affects behavior/scope/acceptance, neutral illustration when helpful, and exact answer instructions. Clarify concerns what and why; design options belong to Analyze. Questions should be batched after reasonable investigation. Reopening a topic changes its revision or records an explicit re-request.

The immutable UTF-8 export starts with title/summary and `Request: <id>`, `Form: <id>`, `Generated: <timestamp>`. Each block retains the authoritative `## Q-ID | revision=...` heading, `Question:` text, explanation, why, instructions, optional illustration, essential/default information, unchecked options, `Answer:` and `Comments:`. Instructions explicitly permit an unknown/discussion answer. File names include request/form/time. Download is passive and proves neither receipt nor answer. Unchanged exports can be reused; prior exports remain available. No outstanding marked requestor questions means no empty export.

Returned files/paste are UTF-8 text, maximum 1 MiB. Screen before persisting originals or logging content. Accepted receipts retain exact original, fingerprint and attribution. Parse only known identities and fields; preserve outside text for review. Match request/form/question ID and revision, never filename/order/guessed meaning. Missing identities require manual association with provenance. Wrong/closed request forms remain unassigned intake under `input/`, without mutating/reopening that request.

Review shows the original question/explanation, existing answer, proposed answer and status: matched, missing, unknown, duplicate, altered, stale, withdrawn, contradictory, or unanswered. Accept, retain, correct or leave unresolved per item. Corrections preserve original and actual reviewer attribution. Blank and unknown responses remain unanswered. New wishes in comments become explicitly linked input/amendment, avoiding duplicate interpretation effects. Receipts never approve plans, enable skills, change instructions or permissions, or start implementation.

Save reviewed answers saves drafts only. Import answers and clarify binds form/question/draft/input/amendment revisions, atomically reserves the action, saves reviewed merge, creates immutable submission and starting run, then launches Clarify. Busy/refreshed review is rejected without merge or queue. A launch failure retains the accepted submission for explicit recovery. Idempotency prevents duplicate effects. The host integration owns reservation/lifecycle; standalone helpers provide deterministic parsing, review, snapshots and revision checks without inventing AIH lifecycle state.
