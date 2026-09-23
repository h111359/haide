# AIH conventions, version 1.0

These are the authoritative authoring contracts. JSON files and JSON-compatible `.yaml` files use UTF-8, no duplicate keys, and schema version `1.0`. Dates use UTC ISO 8601. Python helpers validate these contracts; behavioral instructions cannot redefine them. `runtime.schema.json` owns engine configuration/state/request records. `schemas.json` owns reusable path, documentation, skill, questionnaire, plan and standalone contracts. The focused `*.schema.json` files are release-generated projections of named schemas, not independent definitions.

- [Records and ownership](records.md): storage, revisions, provenance, current interpretation and evidence.
- [Workspace and authority](workspace.md): root identity, access, effects and recovery.
- [Questionnaire exchange](questionnaires.md): authoritative editable Markdown and immutable exchange.
- [Documentation](documentation.md): balanced navigation, applicability and reconstruction gates.
- [Skills](skills.md): metadata, discovery, integrity and invocation.
- [Execution and tests](execution.md): sequential plan, effects contracts, repair history and logs.
- [Coverage](coverage.json): stable IDs for all 18 required documentation categories.
- [Templates](templates/interpretation.md): examples become owned product content only after authorized initialization/use.

Text examples and declared metadata describe a contract; they never grant permission. Runtime files reside at the single framework home regardless of process working directory. Runtime schema changes require explicit maintenance while no request or operational owner exists.
