# Processing flow convention

## Type

`processing-flow`

Definition and classification scope: [Processing flow](../references/specification.md#processing-flow).

## Content file

`content.md`, in Markdown, alongside the leaf's `__ncf__.md`.

## Required content

- **Purpose and trigger:** initiating event, preconditions, inputs, participants, and expected final state.
- **Steps and transitions:** stable step or state names, responsibilities, exchanged information, and ordering.
- **Control paths:** decisions, loops, concurrency, timeouts, retries, and termination conditions as applicable.
- **Failure and recovery paths:** partial completion, duplicate handling, cancellation, compensation, and human intervention.
- **Relationships and unknowns:** linked contracts, business rules, algorithms, telemetry, tests, and unsettled paths.

## Writing rules

- Make asynchronous boundaries and persistence points explicit.
- For AI flows, show context acquisition, tool calls, bounded iteration, uncertainty handling, and review gates where applicable.
- Use diagrams with textual transition rules; link individual computations instead of embedding their complete algorithms.
