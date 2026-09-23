# AIH — Hristo AI development environment

A portable, file-based AI product-development harness. The installed core is in [`.aih/`](.aih/README.md); product state is created separately on first use. No database, Git, Node or PowerShell is required to operate it.

Start the local portal with Python 3.11 or newer:

```bash
python3 -B .aih/engine/cli.py serve --no-browser
```

Open the printed loopback URL. First startup initializes the product and attempts its documentation baseline through the configured profile. If that profile cannot run safely, setup remains visibly pending; configure a compatible agent or use the documented manual handoff. A complete baseline is required before opening a change request.

```bash
python3 -B .aih/engine/cli.py menu
python3 -B .aih/engine/cli.py help
python3 -B .aih/engine/cli.py test
python3 -B .aih/engine/cli.py demo
```

See the [quick start](.aih/README.md), [user guide](.aih/USER_GUIDE.md), [semantic/manual-result contracts](.aih/conventions/semantic-results.md), [validation report](logs/VALIDATION.md), [independent traceability review](logs/TRACEABILITY.md), and [implementation logs](logs/README.md). The original specification and UX references remain in `definitions/`.

Linux execution and containment are tested. Native Windows managed writes/processes currently fail closed; use WSL for the tested enforcement path. Real Codex startup was attempted, but the installed alpha CLI could not start under the required confinement. Synthetic workflow demonstrations and actual product-test subprocesses are reported separately from live agent execution.
