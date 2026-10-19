# Workspace structure convention

## Type

`workspace-structure`

Definition and classification scope: [Workspace structure](../concepts/specification.md#workspace-structure).

## Content file

`content.md`, in Markdown, alongside the leaf's `__ncf__.md`.

## Required content

- **Coverage and context:** the workspace root or roots described, path notation, and any unavailable or unverified areas.
- **Structure map:** every top-level folder and file, including hidden entries, with its meaning and purpose. Include the most important subfolders and files within them selectively. For each entry or group, give its workspace-relative path or explicit pattern, explain what belongs there, and indicate which tasks or questions warrant examining it further.
- **Related guidance:** links to relevant development instructions, architecture descriptions, or existing area guides where they help an agent continue discovery.
- **Evidence and freshness:** observation date, sources or verification method, known gaps, and layout changes that should trigger an update.

## Writing rules

- Describe files with the same purpose only as a group, using a clearly scoped path pattern or directory and explaining their shared role. Describe files with distinct roles separately; avoid enumerating group members.
- Balance discoverability with reading cost. Expand descendants only when their distinct purpose or entry point changes where an agent should look next; stop when a group description or linked area guide provides enough direction.
- Use a compact table or annotated tree with explanations. Avoid exhaustive recursive listings, repeated path descriptions, and explanations of every implementation file.
- Cover generated output, dependencies, caches, and tool metadata briefly by purpose or group; do not expand their contents unless they provide a meaningful navigation entry point.
- Verify paths and purpose using directory entries and targeted authoritative files as needed; do not require reading every file or exhaustively scanning descendants. Mark uncertain meanings and unverified areas explicitly.
- Distinguish observed layout from planned paths, optional local folders, and absent entries; do not present them as existing facts.
- Link canonical instructions, design, and asset registers instead of copying their rules or details. This description guides selective inspection; it does not prescribe reading every listed path.
