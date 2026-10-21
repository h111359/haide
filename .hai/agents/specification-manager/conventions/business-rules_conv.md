# Business rules convention

## Type

`business-rules`

Definition and classification scope: [Business rules](../references/specification.md#business-rules).

## Content file

`content.md`, in Markdown, alongside the leaf's `__ncf__.md`.

## Required content

- **Domain context:** the business subject and terminology needed to interpret the rules.
- **Rules:** stable IDs, applicability, conditions, permitted or prohibited outcomes, and exceptions.
- **Derivations:** business formulas, units, effective periods, and precedence where rules interact.
- **Examples:** representative valid, invalid, and boundary cases.
- **Authority and relationships:** policy owner or source, effective dates, linked features, models, algorithms, and open questions.

## Writing rules

- Express policies independently of screens, services, programming languages, and storage mechanisms.
- Distinguish established rules from assumptions; cite the applicable source for externally imposed obligations.
- Specify conflicts and precedence explicitly rather than allowing implementation order to decide policy.
