# Proposed work plan

Recorded 2026-11-02T06:52:54Z by Activity-manager from Leader-supplied Agent-definition-manager recommendations and the exact user follow-up preserved in input.md. This is a proposed plan, not implementation authorization.

## Direction and decisions

The user supports extracting Chronicle Manager and tentatively suggests `codex-chronicle-manager`. That name is appropriate if the role deliberately owns Codex-specific durable source handling; use a generic name if cross-runtime support is intended. Final naming and source scope remain to be settled.

Package management means installation/update of selected agent packages and their registration in the environment. Recommend retaining it in Environment-manager, together with model-profile management; separate package/profile roles are unnecessary for the present proposal. The user prefers retaining profile functionality in Environment-manager.

Proposed allocation: business analyst owns clarification/requirements; solution architect owns technical analysis/planning; software developer owns implementation; quality assurance owns product verification. Leader retains orchestration. Environment-manager owns core environment administration, model profiles, packages and Activity lifecycle/records. Chronicle Manager owns transcripts, checkpoints and source-coverage verification. The merger and four specialists remain proposals; no creation, installation, registration or implementation has been authorized.

## Short plan

1. Define role contracts, final names, source scope and domain boundaries.
2. Extract substantive execution into the proposed specialist roles and extract chronicles into their selected owner.
3. Move remaining Activity ownership into Environment-manager, preserving bootstrap versus tracked-record prerequisites and Leader-mediated fresh coverage evidence before closure.
4. Update registrations, configuration contracts, routing and references across installed/source consumers while preserving existing Activity identities, records and history.
5. Validate startup, specialist-result recording, transcript synchronization and closure behavior, then retire the old Activity-manager definition after its responsibilities and consumers are migrated.

## Verification and limits

This record captures the supplied planning result without repeating the design review. No implementation or migration tests have run. Product QA remains distinct from record consistency and source-coverage checks. No open dependency prevents recording this plan; final naming/source scope is a proposed implementation decision.

Recording status is separate: the preceding read-only progress inspection found no chronicles directory/checkpoint or durable source metadata. Leader reports the five-prompt threshold reached, but authoritative source identity/path, occurrence boundaries and completed-source cutoff remain unavailable. No transcript batch or coverage is claimed; no transcript writes were assigned.
