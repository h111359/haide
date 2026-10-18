# Workspace instructions

## Chat chronicles

Maintain one Markdown transcript per Codex session in `chronicles/` for this workspace. Update it during the conversation without waiting for the user to request an export.

- Copy user prompts and final assistant responses verbatim, in chronological order, under repeated `## Prompt:` and `## Outcome:` headings.
- Include clarification questions and user answers in their recorded order.
- Never summarize, correct, normalize, or shorten recorded text. Preserve spelling, escaping, whitespace, and formatting.
- Exclude system/developer instructions, environment metadata, tool calls, and intermediate progress messages.
- Use the session start time in `Europe/Sofia` for filenames: `YYYYMMDD_HHMM.md`. Include seconds when necessary to distinguish sessions starting within the same minute.
- Record the source session ID and local transcript path under `## Source:`.
- Update the existing session file without duplicating messages. Use the session ID to identify it, even if the conversation resumes on another date.
- Synchronize completed exchanges from the saved local transcript. Before sending a final response, save its exact text as the next outcome and send that same text to the user.
- Record commit messages under `## Commit message:` only when verified. Never invent a commit message or imply that a commit occurred without evidence.
- Do not create Git commits automatically.
