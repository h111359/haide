# Requirements readiness

This convention is the shared review form for AI and human reviewers. The initial
version has eight categories and 28 mandatory checks with stable identifiers.
Copy the checkboxes into an attributable assessment and attach evidence for each
item; changing a checkbox without evidence does not satisfy it.

## Assessment contract

Apply before downstream technical analysis or implementation planning for a new
request, and reapply after changes to goals, scope or acceptance. Record the
request/Activity UUID, assessed revision or source hash, assessor/source/date,
latest effective decisions, each check's pass/fail and evidence, unresolved
critical gaps, and final status. Host coordinator holds failed requests from
technical analysis, planning and implementation.

Pass requires every current mandatory item satisfied and no undocumented critical
gap. An unsupported assertion is not evidence. An assumption or explicit iteration
deferral can satisfy an item only when it actually resolves that uncertainty;
record the premise, evidence, consequences if false and why no explicit human
judgment is being replaced. Silence/recommendations are never decisions. An
unresolved human decision or critical conflict fails the gate regardless of
checkbox count. Record failed IDs and decisions for further clarification.

Only these two narrow exemptions exist: internal framework upkeep with no
user-visible behavior change (including pure refactoring), or an urgent clear
defect whose repair is one reversible change. Record the qualifying observed
scope, exact exemption and reason; neither grants permission nor removes durable
clarification safeguards. Any broader request uses every mandatory check.

## Mandatory review form

### R1 — Intent

- [ ] **R1.1 Self-contained objective:** One or two sentences explain the goal to a
  new colleague without specialist background or further explanation.
- [ ] **R1.2 Coherent outcome:** One atomic intent is stated; multiple tasks serve
  that outcome rather than combining independent requests.
- [ ] **R1.3 Observable change:** The affected party's outcome or behavior is
  described, rather than only prescribing an internal solution.
- [ ] **R1.4 Motivating need:** The goal connects to a stated business need, user
  problem or product objective, including reliable existing product context.

### R2 — People

- [ ] **R2.1 Identified participant:** At least one user/stakeholder role directly
  using or affected by the change is named.
- [ ] **R2.2 Participant difficulty:** That participant's current problem or unmet
  objective is explained.
- [ ] **R2.3 Other affected parties:** Additional affected parties are identified,
  or their absence is explicitly established.

### R3 — Value

- [ ] **R3.1 Concrete benefit:** At least one user, business or product benefit
  justifies the effort and opportunity cost.
- [ ] **R3.2 Priority rationale:** Priority, urgency, dependency or another reason
  for addressing the request now is recorded rather than invented.
- [ ] **R3.3 Existing capability considered:** A real gap is established, or the
  request explains why an available equivalent needs modification.

### R4 — Delivery boundaries

- [ ] **R4.1 Named deliverables:** Bounded outputs or changes identify affected or
  new files, components or behaviors as appropriate.
- [ ] **R4.2 Iteration-sized work:** The request fits one reasonable implementation
  iteration; independent subrequests are identified for decomposition if needed.
- [ ] **R4.3 Compatible scope:** No deliverables demand mutually exclusive results.
- [ ] **R4.4 Outcome-based scope:** Scope says what must exist or happen, rather
  than dictating how internal code must implement it.

### R5 — Exclusions

- [ ] **R5.1 Explicit exclusion:** At least one concern is expressly out of scope.
- [ ] **R5.2 Precise exclusions:** Exclusions identify concrete features, file
  types, workflows or components rather than undefined broad labels.

### R6 — Limits and premises

- [ ] **R6.1 Technical limits:** Known restrictions, such as supported versions,
  allowed formats and available tools, are listed.
- [ ] **R6.2 Organizational limits:** Applicable policies, naming rules, process
  obligations and compliance constraints are recorded.
- [ ] **R6.3 Consequential assumptions:** Premises affecting scope, approach or
  acceptance are documented with consequences/risks if false.
- [ ] **R6.4 Separate constraints:** A dedicated section keeps constraints distinct
  from functional deliverables.

### R7 — Evidence of success

- [ ] **R7.1 Completion test:** At least one acceptance condition is defined.
- [ ] **R7.2 Objective verification:** Each condition has a deterministic pass/fail
  check using a named artifact, behavior, count or observable state.
- [ ] **R7.3 Feasible acceptance:** Conditions are achievable within the stated
  scope and constraints.
- [ ] **R7.4 Specific language:** Undefined quality claims are replaced by
  measurable thresholds or explicit observable behavior.
- [ ] **R7.5 Full scope coverage:** Every deliverable maps to an acceptance condition.

### R8 — Consistency with product knowledge

- [ ] **R8.1 Shared framing:** Domain, actors, vocabulary and product boundaries
  match the established context.
- [ ] **R8.2 Prior decisions:** Applicable decisions, conventions and restrictions
  appear in constraints/assumptions; any relevant context deemed inapplicable is
  explicitly explained.
- [ ] **R8.3 Resolved conflicts:** Scope and acceptance are compared with product
  constraints; discrepancies are resolved or escalated as documented blockers.
  An unresolved blocker cannot be represented as a pass.

## Compatible extension

Append new annotated checkboxes at the end of their existing category, before the
next section boundary, using its next unused item ID. Append a new category after
existing categories and before this extension section, using the next category
number, a short explanation and at least one annotated checkbox explaining what
evidence satisfies it. New items are mandatory for new/current reassessments.

Preserve all existing identifiers, ordering, references and historical reviews.
Never delete, renumber or restructure old entries in a way that breaks them.
Initial publication assigns these stable IDs; a new edition records additions
without rewriting old assessments. A prior pass is evidence for its assessed
version, not an automatic pass for an extended or changed request.

The pure helper `readiness_items` checks initial identifier/order preservation and
ordered additions. `assess_readiness` evaluates supplied evidence for every current
item; it cannot establish the truth or adequacy of that evidence. Reviewers remain
responsible for semantics and consequential assumptions.
