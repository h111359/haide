# Procedure

## Definition

A [term:Procedure] is an agent-owned workflow that turns supplied inputs into
observable outputs through explicit actions and conditional branches, within the
agent's responsibilities and the user's agreed task and permission.

## Purpose

Make work reviewable by separating what information is needed, what must already
hold, what requirements and choices apply, what actions follow, and what evidence constitutes
an outcome. A procedure is a human-readable contract, not an execution engine.

## Explanation

### Selection and identity

A trigger identifies when a procedure is applicable. It is neither permission to
act nor priority or execution order; dependencies must be stated explicitly.
Executing a procedure keeps the same agent identity and does not create another
agent invocation, delegation, or registration.

An agent with multiple procedures keeps each in a separate owned file and selects
them through its `SKILL.md` index. An agent with one procedure may keep it inline
or use the same indexed-file form. The canonical trigger occurs at that selection
point. A short description of one or two sentences explains the procedure's
specific purpose and intended result rather than repeating its trigger.

### Entry conditions, obligations, and actions

Prerequisites are conditions required before execution. Shared rules in `SKILL.md`
apply to all the agent's procedures; local rules describe only requirements,
prohibitions, or choices specific to one procedure. A local rule cannot override a shared rule, grant extra permission, or
substitute for another owner's contract. Applicability and exceptions belong to
the rule that declares them; locality and file order do not establish precedence.

Rules use readable titles without IDs. Optional subject groups aid review, not
priority. Titles are unique within their own Rules section. A mandatory local
Rules section containing `None.` means no additional local rules; it never
disables shared rules. Repeating a shared instruction locally creates competing
maintenance points rather than a stronger safeguard.

A rule can require an action (`MUST`), prohibit it (`MUST NOT`), or permit a choice
(`MAY`). Permission is different from ability: an available tool does not make an
action permitted. `MAY` describes an allowed choice within the existing task and
permission, not a new grant. Conditions such as IF, WHEN, and ONLY IF explain
applicability or timing rather than weakening or strengthening the rule.

Explicit wording helps distinguish obligations from facts and preferences. It
does not make an unclear actor, missing condition, or invented permission correct.
A preference can be explained as a default with its existing permitted alternatives;
turning it into a requirement would change the policy. The writing convention
defines the exact words and plain-language style while authoring procedures own
the review. Concepts remain explanations rather than being forced into rule wording.

Steps are ordered actions and explicit branches. Information is supplied before
an action consumes it; absence, conflict, and failure branches are stated where
they affect dependent actions. Ongoing obligations, entry conditions, and concept
explanations are not numbered as steps. Concepts explain meaning and rationale;
conventions define reusable formats and contracts rather than agent workflows.

### Inputs, outputs, and named references

Each procedure owns its inputs and outputs. An input is Mandatory or Optional;
an operation-specific prerequisite or rule can require an otherwise optional
value for that operation. Optional does not mean every operation can proceed
without it. Sources and absence behavior make missing context explicit, without
inventing defaults or permission. Outputs distinguish completed, partial, pending,
and unavailable results through observable completion evidence.

`[input:task]` and `[output:result]` identify entries in the current procedure's
own tables. `[term:Procedure]` identifies a declared concept source rather than a
supplied value. These namespaces distinguish meanings for human readers: they
are literal named references, not a template language or automatic substitution.
Agent-level concept mappings are available to its procedures; procedure-local
additions do not redefine inherited terms. There are no agent-global input/output
parameters. A call to another procedure explicitly binds source values/evidence
to the destination's input names; identical names alone imply no passing or
inheritance. The notation convention defines the exact spelling and declarations.

Readable structure supports verification but cannot prove that an obligation is
correctly scoped, that steps are sufficient, or that evidence satisfies the human's
objective. Those remain semantic review and execution responsibilities.

## Supporting Terms

- [term:Prerequisite]: a condition that must hold before the dependent execution begins.
- [term:Rule]: a requirement, prohibition, or permission that applies within its explicitly declared scope and conditions.
- [term:Step]: an action or conditional branch in the execution workflow.

## References

- [Agent concept](agent.md): role identity, ownership, registration, and delegation.
- [Procedure convention](../conventions/procedure_conv.md): exact external/inline structure and supported authoring subset.
- [Reference notation](../conventions/reference-notation_conv.md): literal namespaces, declarations, local scope, and explicit passing.
- [Instruction writing](../conventions/instruction-writing_conv.md): strict rule vocabulary and clear wording without changing meaning.
