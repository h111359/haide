# BL-0007 clarification

Observed: backlog/new/BL-0007.md requests a more specific name for the workspace-local advisor because additional advisors are desired. Why and acceptance criteria were unspecified. The registered .hai_env/agents/advisor/SKILL.md reviews this repository's .hai/ framework and recommends the top three next actions without changes or coordination. No matching hai_agents_library/agents/advisor source package exists; the installed definition is the selected workspace-local authoring target.

Proposed name: hai-framework-advisor. Proposed business outcome: users can distinguish HAI framework advice from future advisors. Proposed scope: rename the existing workspace-local role without changing its responsibilities or creating additional advisors. These proposals are not yet user-approved. Clarification is direct host analysis; no sub-agent spawned and no advisor review was invoked, so its full-framework-review procedure was not executed.

Proposed acceptance criteria:
1. The chosen explicit name is consistent across folder, definition identity, configuration contract identity, current registration and active references.
2. The role remains discoverable under its new name and its selection guide explains the existing framework-specific purpose.
3. Existing behavior and read-only restrictions are preserved; no additional advisor is created.
4. Existing external settings are preserved if present, with any name-based path transition explicitly handled. The expected old override file is currently absent.
5. No duplicate current registration or obsolete live identity remains; historical Activity/backlog evidence retains original names as history.
6. Definition, catalogue and core startup checks pass after implementation.

Pending decision: preferred new name. Rename-only scope is proposed from the original story; changes to review behavior or distribution remain separate unless the user expands scope. No rename, package install or registration mutation has been performed.


Revision provenance: source: User: Let’s work to clarify BL-0007; existing backlog item and advisor definition; reason: Capture clarification evidence and pending decisions; reason: Record observed scope and clearly separate proposed clarification from accepted requirements; recorded 2026-11-07T16:57:40Z.
