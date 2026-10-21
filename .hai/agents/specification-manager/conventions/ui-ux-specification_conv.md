# UI/UX specification convention

## Type

`ui-ux-specification`

Definition and classification scope: [UI/UX specification](../references/specification.md#uiux-specification).

## Content file

`content.md`, in Markdown, alongside the leaf's `__ncf__.md`. Link canonical mockups and design assets rather than placing extra payload files in the leaf.

## Required content

- **Users and tasks:** relevant user groups, contexts, goals, and linked functional requirements.
- **Navigation and layout:** information hierarchy, entry points, screens or conversation surfaces, and design references.
- **Interaction behavior:** controls, transitions, loading, empty, success, validation, and failure states.
- **Presentation and inclusion:** content, visual rules, responsive behavior, keyboard and assistive interaction, and localization.
- **Validation and unknowns:** linked quality targets, usability or accessibility checks, and unresolved design questions.

## Writing rules

- Describe behavior in text even when a mockup exists; identify which design source is authoritative.
- For conversational AI, define turn behavior, uncertainty communication, disclosures, review controls, and recovery from misunderstood input.
- Link capabilities and measurable targets instead of duplicating requirements.
