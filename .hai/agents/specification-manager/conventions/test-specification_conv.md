# Test specification convention

## Type

`test-specification`

Definition and classification scope: [Test specification](../references/specification.md#test-specification).

## Content file

`content.md`, in Markdown, alongside the leaf's `__ncf__.md`. Link executable tests, fixtures, and evaluation datasets maintained in the workspace.

## Required content

- **Verification scope:** linked requirements, risks, exclusions, and test levels or methods.
- **Setup:** environment, tools, fixtures, data sources, isolation, and cleanup needs.
- **Cases:** stable case IDs, preconditions, actions or inputs, expected observations, and pass or fail rules.
- **Coverage and evaluation:** traceability, boundary cases, sampling, metrics, tolerances, and limitations.
- **Execution and evidence:** how to run checks, where results are stored, canonical test links, and unresolved coverage gaps.

## Writing rules

- Link normative requirements and thresholds; distinguish coverage gaps from product defects.
- For AI evaluations, record dataset provenance, evaluation version, judge method, variability, and safeguards against evaluation-data leakage.
- Keep transient test-run logs outside the specification; document durable verification methods and reference relevant evidence.
