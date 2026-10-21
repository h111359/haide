# User documentation convention

## Type

`user-documentation`

Definition and classification scope: [User documentation](../references/specification.md#user-documentation).

## Content file

`content.md`, in Markdown, alongside the leaf's `__ncf__.md`. Link canonical images, examples, and other supporting assets outside the leaf.

## Required content

- **Audience and purpose:** user group, task or topic, supported product versions, and expected prior knowledge.
- **Prerequisites and concepts:** access, configuration, terminology, and relevant limitations.
- **Instructions or explanation:** ordered task steps, examples, feature behavior, or user-visible release changes appropriate to the topic.
- **Results and troubleshooting:** expected outcome, common mistakes, recovery options, and support routes as applicable.
- **Related material and gaps:** tutorials, reference contracts, relevant feature links, and known documentation limitations.

## Writing rules

- Write from the consumer's perspective and keep internal implementation detail out unless it helps complete the task.
- Explain AI limitations and review responsibilities when they affect user decisions.
- Link normative contracts and behavior specifications; document source contribution in Development guide instead.
