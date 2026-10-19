# Workspace instructions

## Chat chronicles

Chronicles are optional. Use `features.chronicles.enabled` and
`features.chronicles.location` from validated compatible `.hai_env/state.json`.
The default configured location is `.hai_env/chronicles`. When disabled, do
not create or update transcripts. If state is absent, invalid, or incompatible,
report the unresolved setting instead of assuming recording is enabled.

When enabled, leader delegates transcript maintenance to the shared
[chronicles-manager](.hai/agents/chronicles-manager/knowledge.md), whose
canonical procedures govern synchronization and verification. Maintain one
Markdown transcript per Codex session at the configured location and update
it during the conversation without waiting for an export request. Apply these
recording requirements only when chronicles are enabled:

- Copy user prompts and final assistant responses verbatim, in chronological order, under repeated `## Prompt:` and `## Outcome:` headings.
- Include clarification questions and user answers in their recorded order.
- Never summarize, correct, normalize, or shorten recorded text. Preserve spelling, escaping, whitespace, and formatting.
- Exclude system/developer instructions, environment metadata, tool calls, and intermediate progress messages.
- Use the session start time in `Europe/Sofia` for filenames: `YYYYMMDD_HHMM.md`. Include seconds when necessary to distinguish sessions starting within the same minute.
- Record the source session ID and local transcript path under `## Source:`.
- Update the existing session file without duplicating messages. Use the session ID to identify it, even if the conversation resumes on another date.
- Synchronize completed exchanges from the saved local transcript. Before sending a final response, save its exact text as the next outcome and send that same text to the user.
- Record commit messages under `## Commit message:` only when verified. Never invent a commit message or imply that a commit occurred without evidence.

Do not create Git commits automatically, regardless of the chronicles setting.
