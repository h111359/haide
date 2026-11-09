# HAI

HAI is a framework for AI-assisted development. Its reusable Python runtime and contracts live in `.hai/`; persistent workspace configuration, instructions and Activity records live in `.hai_env/`. Product code and durable specifications remain in their own workspace locations.

HAI confines its file changes to the current workspace unless the user explicitly
permits an outside location and purpose. The [workspace write boundary](../conventions/workspace-boundary_conv.md)
applies to hosts, agents and tools, including temporary files and indirect writes;
filesystem access alone is not authorization.

Across software, documents, research, flows and other operations, HAI places
deliverables in their established destinations and keeps task working material
and evidence with its owning work context. The shared [artifact placement contract](../conventions/artifact-placement_conv.md)
defines the distinction by purpose, ownership and lifetime rather than filenames.

The host coordinator interprets the user's request and supplies authorized operations and evidence to the runtime. The runtime validates and manages supported environment, Activity and source-backed recording operations; the host assigns sources and boundaries. Optional workspace extensions provide domain-specific instructions and tools; they are not prerequisites for core startup or administration.

Concepts explain meanings, conventions define formats and contracts, and runtime commands implement documented operations. See [environment](environment.md), [Activity](activity.md), [framework layout](../conventions/framework-layout_conv.md), and [runtime commands](../tools/runtime/README.md).
