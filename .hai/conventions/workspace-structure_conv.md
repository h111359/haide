# Workspace structure convention

## Type

`workspace-structure`

Definition and classification scope: [Workspace structure](../concepts/specification.md#workspace-structure).

## Content file

`content.md`, in Markdown, alongside the leaf's `__ncf__.md`.

## Required content

- **Coverage and context:** the workspace root or roots described, path notation, and any unavailable or unverified areas.
- **Structure map:** top-level folders and files, including hidden entries, subject to the discovery boundaries below. Include the most important permitted subfolders and files selectively. For each entry or group, give its workspace-relative path or explicit pattern, explain what belongs there, and indicate which tasks or questions warrant examining it further.
- **Related guidance:** links to relevant development instructions, architecture descriptions, or existing area guides where they help an agent continue discovery.
- **Evidence and freshness:** observation date, sources or verification method, known gaps, and layout changes that should trigger an update.

## Discovery boundaries

Apply these boundaries to workspace registration, directory maps, and
reverse-engineering implementation into product specifications, in this
order:

1. Exclude workspace-root `.hai/` and `.hai_env/` and all their descendants.
   Do not register these folders or infer product behavior from their
   contents. This does not prevent reading governing HAI instructions,
   using environment context, or reading and maintaining the established
   specification, including one stored under `.hai_env/`.
2. Represent third-party coding libraries, including vendored code, and dependency trees only by
   their top folder and a brief purpose. This limited root entry is
   permitted even when that library folder is gitignored; never enumerate,
   register, inspect, or reverse-engineer its descendants. Establish the
   root and purpose from authoritative manifests, lockfiles, configuration,
   or reliable documentation outside excluded descendants. First-party
   product source is not a third-party library merely because its folder
   is named `lib` or `libraries`; mark unresolved classifications explicitly.
3. Exclude all other gitignored folders and their descendants from
   registration and reverse-engineering. Evaluate effective Git ignore
   rules, including nested `.gitignore` files, precedence, and negation;
   do not use a fixed list of folder names. Follow Git's treatment of
   excluded parents when evaluating negation. Report unavailable ignore
   evidence rather than claiming complete coverage.

These exclusions take precedence over coverage and selective expansion
rules. A brief coverage note may explain an exclusion category without
listing its folders or contents.

## Writing rules

- Describe files with the same purpose only as a group, using a clearly scoped path pattern or directory and explaining their shared role. Describe files with distinct roles separately; avoid enumerating group members.
- Balance discoverability with reading cost. Expand descendants only when their distinct purpose or entry point changes where an agent should look next; stop when a group description or linked area guide provides enough direction.
- Use a compact table or annotated tree with explanations. Avoid exhaustive recursive listings, repeated path descriptions, and explanations of every implementation file.
- Cover permitted generated output, caches, and tool metadata briefly by purpose or group. Keep libraries to top-folder entries and omit excluded areas according to the discovery boundaries; a navigation entry point does not override those limits.
- Verify paths and purpose using directory entries and targeted authoritative files as needed; do not require reading every file or exhaustively scanning descendants. Mark uncertain meanings and unverified areas explicitly.
- Distinguish observed layout from planned paths, optional local folders, and absent entries; do not present them as existing facts.
- Link canonical instructions, design, and asset registers instead of copying their rules or details. This description guides selective inspection; it does not prescribe reading every listed path.
