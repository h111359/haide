from pathlib import Path
root=Path.cwd(); library=root/'hai_agents_library/agents'

def write(agent, path, text):
    p=library/agent/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.rstrip()+'\n',encoding='utf-8')

def procedure(agent, filename, title, description, extra_inputs, prereqs, steps, output, rules='None.'):
    rows=[('workspace_root','Explicit validated workspace root.','Mandatory','Host coordinator.','Retrieve before dependent work.'),('instructions','Fixed and applicable workspace/session instructions.','Mandatory','Caller and readable fixed instructions.','Empty readable file is valid; missing instructions block dependent work.'),('authority','Actual human task, scope, constraints and permissions.','Mandatory','Human request relayed by host.','Retrieve existing authority; never invent permission.'),('activity_context','Validated core state, stable active Activity and relevant current records.','Mandatory','Host and runtime evidence.','Return missing dependency; no standalone bypass.')]+extra_inputs
    inputs='\n'.join('| [input:%s] | %s | %s | %s | %s |'%r for r in rows)
    content=f'''# {title}

## Description

{description}

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
{inputs}

## Prerequisites

Validated selected configuration, mandatory instructions, compatible environment, stable active Activity and meaningful authorized assignment. {prereqs}

## Rules

{rules}

## Steps

1. Establish [input:workspace_root], [input:instructions], [input:authority] and [input:activity_context]; retrieve authorized missing context and stop dependent work on unresolved prerequisites.

'''+ '\n\n'.join(f'{i}. {step}' for i,step in enumerate(steps,2))+f'''

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:work_result] | {output} | Actual results, evidence, current identity and unresolved dependencies are distinct; host persists canonical records. |

## References

- [Role definition](../SKILL.md) — inherited safeguards and conditional references; required throughout.
'''
    write(agent,'procedures/'+filename+'.md',content)

common_rules='''- **Current evidence.** {role} MUST compare readiness and decisions with the current input revision rather than reuse a stale pass.
- **Context authority.** {role} MUST treat assessments, project knowledge and retained history as evidence, never as permission to expand current task scope.
- **Relevant context.** {role} MUST use the Business analyst [context registry contract](../business-analyst/conventions/context-registry.md) for designated supplemental context, inspect supplied relevant readable materials fully and report unreadable or nontext limits.
- **Required conventions.** {role} MUST load the coding, language, framework, interface and documentation conventions applicable to the actual targets before their dependent edits or checks; missing mandatory conventions block only dependent work.
- **Readiness evidence.** {role} MUST require current passed business-readiness evidence or an evidenced exemption under the Business analyst [readiness contract](../business-analyst/conventions/requirements-readiness.md) before dependent technical planning or implementation.
- **Decision provenance.** {role} MUST distinguish human choices, applicable governing instructions and choices actually delegated by the caller; recommendations, preselection and silence MUST NOT count as answers.
- **Framework protection.** {role} MUST follow the Business analyst [protection contract](../business-analyst/conventions/framework-protection.md), preserve covering human authority verbatim and return unauthorized protected changes without reverting them.
- **Workspace boundary.** {role} MUST follow the core [workspace write boundary](../../../.hai/conventions/workspace-boundary_conv.md) for direct and indirect writes, temporary material, caches and cleanup.
- **Encountered concerns.** {role} MUST retain individually reviewable material concerns encountered during scoped research, including unrelated concerns, without treating discovery as authority to repair them.
- **Peer dependencies.** {role} MUST resolve required peer contracts from validated installed siblings and return missing dependencies without executing source-library packages or copying alternate authorities.
'''
for agent,role in [('solution-architect','Solution architect'),('software-developer','Software developer')]:
    p=library/agent/'SKILL.md';s=p.read_text()
    start=s.index('## Procedures')
    s=s[:start]+common_rules.format(role=role)+'\n'+s[start:]
    if agent=='solution-architect':
        s=s.replace('Technical analysis, existing-system assessment, solution architecture, alternatives, interfaces, dependencies and implementation/verification planning.','Technical assessment, evidence acquisition, technical decision analysis and revisions, and self-contained implementation/verification planning in normal or explicitly selected accelerated mode.')
        s=s.replace('| Perform assigned work | An authorized solution architect assignment or follow-up is supplied. | [Perform assigned work](procedures/perform-assigned-work.md) |','''| Assess solution | A new or changed technical assignment needs assessment. | [Assess solution](procedures/assess-solution.md) |
| Resolve technical decisions | A consequential unresolved or changed technical decision needs clarification. | [Resolve technical decisions](procedures/resolve-technical-decisions.md) |
| Prepare implementation plan | A normal or explicitly accelerated implementation plan is requested. | [Prepare implementation plan](procedures/prepare-implementation-plan.md) |''')
        s=s.replace('## Procedures','''- **Decision boundaries.** Solution architect MUST return missing business decisions and unassigned consequential technical choices through the host; choices already delegated MAY be resolved with disclosed reasoning and provenance.
- **Planning only.** Solution architect MUST return proposed assessment, decisions and plan content through the host without modifying product implementation artifacts or granting implementation permission.
- **Dialogue persistence.** Solution architect MUST follow the Business analyst [dialogue contract](../business-analyst/conventions/clarification-dialogue.md), requiring verified host persistence before displaying new questions or applying answers.
- **Plan coherence.** Solution architect MUST carry every implementation-relevant assumption, decision, acceptance obligation and documentation change directly into the current plan and preserve predecessor evidence through host runtime revisions.

## Procedures''')
        s+='''\n- [Technical assessment](conventions/technical-assessment.md) — required for assessment and technical readiness.
- [Plan helper](scripts/README.md) — required before validation; pure structural checks do not prove semantic readiness.
- Business analyst conventions linked in Rules — required for the named operations; absent peers block dependent work only.
'''
    else:
        s=s.replace('Scoped product implementation, necessary developer investigation, fixes and appropriate developer checks.','Current-plan or explicitly authorized substantive direct execution, necessary developer investigation, bounded fixes, developer verification and attributable delivery evidence.')
        s=s.replace('| Perform assigned work | An authorized software developer assignment or follow-up is supplied. | [Perform assigned work](procedures/perform-assigned-work.md) |','''| Validate execution input | A new directive or changed current execution context is supplied. | [Validate execution input](procedures/validate-execution-input.md) |
| Implement assigned work | Current validated directive and runtime implementation-start evidence are available. | [Implement assigned work](procedures/implement-assigned-work.md) |
| Verify and hand off | Implementation results need acceptance checks or a delivery report. | [Verify and hand off](procedures/verify-and-handoff.md) |''')
        s=s.replace('## Procedures','''- **Execution directive.** Software developer MUST implement only the current plan or an explicitly authorized substantive direct directive; assessment/knowledge reads MUST NOT supply missing execution semantics.
- **Plan integrity.** Software developer MUST NOT rewrite its governing plan to justify a deviation; consequential conflicts or changes require host resolution and refreshed directive validation.
- **Actual implementation start.** Software developer MUST require host-returned runtime evidence of the original Activity implementation-start marker before implementation changes or tests and preserve it through retries.
- **Delivery evidence.** Software developer MUST follow the [execution evidence contract](conventions/execution-evidence.md), trace its own direct/indirect changes against the baseline and withhold verified success while mandatory checks or owner work remain unresolved.
- **No independent acceptance.** Software developer MUST return required independent review and managed specification/history work through the host, without claiming its own checks establish independent product acceptance or Activity closure.

## Procedures''')
        s+='''\n- [Execution evidence](conventions/execution-evidence.md) — required for preflight and delivery.
- [Execution helper](scripts/README.md) — required before helper use and interpreting its limits.
- [Architect plan contract](../solution-architect/conventions/implementation-plan_conv.md) — required in plan mode; missing peer does not block independent direct-mode diagnosis.
- Business analyst conventions linked in Rules — required for the named operations; absent peers block dependent work only.
'''
    p.write_text(s)

work=('work_context','Current requirements, acceptance, evidence sources, attachments and decisions.','Mandatory','Host and authorized task sources.','Retrieve facts; return unresolved necessary decisions.')
procedure('solution-architect','assess-solution','Assess solution','Research the current technical request and prepare an attributable assessment with readiness evidence.',[work], 'Current business-readiness evidence is available before dependent technical planning.',[
'Compare [input:work_context] with the current input and decision evidence. Identify affected people, intent, boundaries, constraints and measurable acceptance; consume all applicable business-readiness checks, not an assumed prior pass.',
'Inventory supplied and nested attachments, designated context and relevant project conventions. Read authorized readable materials completely, distinguish placeholders, and identify nontext/unreadable limits. Follow the registry contract for supplemental sources; registry Prompt/Update metadata grants no execution or write authority.',
'Inspect relevant implementation, interfaces, data, existing patterns and operational constraints before asking for discoverable facts. Use authorized external research for real external factual gaps; separate findings from decisions. Record distinct material defects, inconsistencies, duplication, broken references and risks encountered without expanding repair scope.',
'Analyze feasible options, edge/empty/boundary conditions, first use and revision, migration/compatibility, failure and recovery behavior. Explain knowledge conflicts and how existing intent is preserved or explicitly changed. Identify knowledge deltas and required owners.',
'Prepare the ordered assessment sections and T1–T6 evidence under the technical assessment convention. Mark unresolved choices and dependent actions explicitly. If a consequential decision needs clarification, pass the assessment and choices to host for Resolve technical decisions as assessment and decisions.',
'Request host persistence with original input references and revision provenance. Use plan_contract.py for structural/readiness diagnostics after reading its README; correct authorized draft problems, but keep unresolved readiness blocked. Return actual evidence and checks; do not publish a false ready assessment.'
], 'Proposed assessment, source identities, findings, decisions, readiness results and unresolved dependencies.')
procedure('solution-architect','resolve-technical-decisions','Resolve technical decisions','Prepare focused technical clarifications and apply verified decisions to the current assessment.',[
('assessment','Current attributable assessment and relevant source identity.','Mandatory','Assess solution result relayed by host.','Return inconsistent/missing assessment; do not reconstruct history.'),
('decisions','Unresolved alternatives or actual revised answers with provenance.','Mandatory','Host and current ledger.','Retrieve current ledger before proposing new questions.')], 'Verified current assessment and accessible host dialogue persistence handshake.',[
'Compare [input:assessment] and [input:decisions] with current Activity input and the saved dialogue ledger. Retrieve facts before questions; distinguish already settled choices from choices actually delegated and unresolved human decisions.',
'For each necessary unresolved decision prepare named alternatives, benefits, costs, implementation impact and a recommendation. Keep assessment alternatives neutral and recommendation separate; avoid quotas or questions for safely delegated implementation details.',
'Prepare the existing dialogue contract events with host-supplied occurrence identities and stable ledger IDs. Return candidates to host for serialized runtime persistence and exact readback; display only verified saved question blocks. Reuse unanswered IDs and split UI batches without duplicate questions.',
'Apply only host-verified actual answers. Preserve raw multipart responses and revisions; ambiguous mapping, recommendations, silence or unchecked fields are not answers. Return unresolved mappings and hold dependent finalization.',
'Reassess every affected assumption, alternative, action, acceptance condition and knowledge change. Ask host to retain predecessors using runtime revisions and persist the coherent current assessment. If there is no new input or answer, return no new work without manufacturing a revision.',
'Return the current assessment, effective decision identity and remaining dependencies to host; pass those values as assessment and work_context for Prepare implementation plan only when required readiness holds.'
], 'Verified effective decisions or proposed questions, revised assessment and explicit pending answers.')
procedure('solution-architect','prepare-implementation-plan','Prepare implementation plan','Prepare a self-contained implementation brief that preserves current requirements, decisions and execution boundaries.',[
work,('assessment','Current assessment and technical-readiness evidence.','Optional','Host and Assess solution result.','Required in normal mode; accelerated mode derives the same evidence from current authorized sources.'),
('mode','normal or explicitly requested accelerated planning.','Optional','Actual caller instruction.','Default normal; no implied accelerated authority.')], 'Passed business readiness or its evidenced narrow exemption. Normal mode has current assessment; accelerated mode has explicit selection and equivalent readiness evidence.',[
'Confirm [input:mode] against actual [input:authority], defaulting to normal. Compare [input:work_context] and any [input:assessment] with current input/decisions; stop dependent finalization on stale evidence or unresolved critical decisions. Explicit acceleration omits a separate assessment artifact, not required checks or permissions.',
'Build one coherent plan using the implementation-plan convention: execution contract, acceptance criteria, overview, seven-part phases and exact file inventory. Preserve all settled decisions, assumptions, constraints, authorization statements, task dependencies and cross-artifact conditions. Disclose every choice actually delegated.',
'Give every task a target, operation, expected result, dependency reason, acceptance mapping and completion check. Specify commands/tools and output destinations for executable operations. Keep essential semantics directly in the plan; natural-language instructions precede implementation code, and unavailable references cannot carry required work.',
'Include knowledge/documentation deltas with target identity, exact structured edits where required, preserved intent and owner validation. Prefer staged owner-controlled replacement over destructive delete-then-insert; if no documentation update is needed state why. Include proportionate tests and explicit human/external acceptance methods.',
'Validate structure and current identity through plan_contract.py and independently review semantic completeness, feasibility, ordering and permissions. A blocked proposal remains labeled blocked; do not repair meaning automatically or treat a structural pass as authorization.',
'Return plan and validation evidence to host for serialized persistence and predecessor retention. Recheck source/decision identity before accepting host readback; keep prior plans as history rather than merging conflicting instructions. Planning does not authorize implementation.'
], 'Proposed current plan, input/decision identity, validation evidence and execution-readiness dependencies.')
procedure('software-developer','validate-execution-input','Validate execution input','Validate the current directive and execution dependencies before implementation begins.',[
('directive','Current plan or substantive explicitly authorized direct directive.','Mandatory','Host current assignment.','Reject absent/empty/template-only input; never infer work from history.'),
('current_context','Current source/decision hashes, actual authority, modes and dependency evidence.','Mandatory','Host and runtime evidence.','Retrieve current facts before dependent execution.')], 'Current directive and actual human implementation authority.',[
'Compare [input:directive] and [input:current_context] with current host input, effective decisions and acceptance. In plan mode require the installed architect contract; in direct mode require explicit selection and complete Outcome/Scope/Constraints/Acceptance/Tasks/Verification/Documentation sections. A clear instruction to implement substantive bounded work can select direct mode without a magic phrase.',
'Load relevant project knowledge as supplementary evidence and applicable coding, language, framework, interface and documentation conventions. Classify mandatory versus optional dependencies; report optional absence without blocking independent work.',
'Capture baseline content/path evidence and identify planned direct and indirect writes, temporary files and caches. Validate workspace destinations and links; require exact covering human authorization for protected maintenance and any outside location/purpose. A generated task or permissive sandbox cannot authorize itself.',
'Require host-returned implementation-start evidence before implementation changes or tests. Confirm required owner dependencies and current business-readiness evidence. Run execution_contract.py with the actual directive and current context after reading its README; host verifies semantic permission and completeness beyond helper structure.',
'Return validated directive identity and actual dependency checks as work_result. On contradictions or stale/missing inputs return affected blockers; do not edit the governing plan or silently obtain task semantics from its assessment.'
], 'Validated current execution input or attributable preflight blockers.')
procedure('software-developer','implement-assigned-work','Implement assigned work','Implement bounded current work while preserving scope, dependencies and attributable change evidence.',[
('validated_input','Current validated directive, scope, identity and preflight results.','Mandatory','Validate execution input result relayed by host.','Return preflight dependency; do not begin product edits.')], 'Current preflight and original runtime implementation-start evidence.',[
'Recheck [input:validated_input] against current source/decisions, runtime marker and destination baseline before writes. Return changed identity for refreshed preflight rather than relying on an old validation result.',
'Execute the directive tasks in dependency order at canonical locations. Use authorized Activity/invocation scratch for helpers and configure caches before tools. Keep a per-task result and direct/indirect changed-path evidence; preserve unrelated existing modifications.',
'Investigate failures and correct authorized implementation defects, rerunning affected checks. Stop dependent work on mandatory tool failure, changed inputs or partial persistence failure; preserve partial bytes and diagnostics without automatic rollback or retry of the partial operation.',
'Return consequential deviations or newly discovered scope/permission conflicts through host for a coherent revised directive. Record out-of-scope concerns separately. Never rewrite the governing plan to authorize different behavior.',
'Provide concise progress at completed meaningful tasks. Return implementation notes, actual changes, decisions, checks and blockers to host as implementation_result for Verify and hand off; do not advance Activity state yourself.'
], 'Implementation results, attributable changed paths, task progress, checks and partial failures.')
procedure('software-developer','verify-and-handoff','Verify and hand off','Verify the delivered changes and return accurate completion evidence and remaining dependencies.',[
('implementation_result','Actual directive identity, task results, changed paths and observed checks.','Mandatory','Implement assigned work result relayed by host.','Retrieve actual evidence; never infer completion.')], 'Current implementation evidence and applicable verification obligations.',[
'Compare [input:implementation_result] with the current directive and acceptance criteria. Inspect each artifact/operation, baseline attribution and direct/indirect effects, including generated/untracked/deleted/moved paths; do not charge unchanged pre-existing edits to this run.',
'Run meaningful automatic tests and document/knowledge validation required by the directive and conventions. Identify human/external acceptance methods. Record passed, failed, skipped and unavailable checks separately; investigate and correct authorized failures and rerun affected checks only.',
'Return agreed managed knowledge/history updates and required independent review through host. Keep required owner work pending until actual validated evidence returns; disabled specification is not permission to enable or silently omit required work. Record why no knowledge update was needed where applicable.',
'Inspect protected paths against baseline and exact covering authority using the existing protection contract. Report unauthorized paths in stable order and stop affected success handoff without reverting them. Check workspace boundaries and outside-write provenance, including indirect tool effects.',
'Prepare execution evidence and run execution_contract.py with the current directive/context/evidence. Verify all required tasks, checks and owner dependencies are represented, not merely a convenient subset. A failed mandatory history operation remains a blocker under existing no-automatic-retry safeguards.',
'Return verified, blocked or partial result with exact artifacts, task outcomes, actual checks, decision provenance, limitations and known usage-source availability. Host owns runtime persistence, recording synchronization, independent acceptance and any separately authorized closure; no future outcome is fabricated.'
], 'Delivery evidence with verified/blocked/partial status, current artifacts and unresolved acceptance risks.')
for agent in ['solution-architect','software-developer']:
    (library/agent/'procedures/perform-assigned-work.md').unlink()
