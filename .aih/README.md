# AIH — file-based product development harness

AIH keeps one product's requirements, sequential implementation, tests, documentation and recovery evidence in files. A product may span explicitly registered writable and read-only folders. Git and a database are optional; the core is `.aih/`, and runtime information is centralized in `.aih_product/`.

From the framework home, with Python 3.11 or newer:

```sh
python -B .aih/engine/cli.py help
python -B .aih/engine/cli.py init
python -B .aih/engine/cli.py serve --port 8765 --no-browser
```

Open the printed local portal URL. For the shared interactive menu run `python -B .aih/engine/cli.py menu`, or use `.aih/menu.sh` on Linux and `.aih\menu.cmd` on Windows. On Windows, `py -3 -B` may replace `python -B`. From another directory use the absolute CLI path and `--home /absolute/framework/home` before the command. Quote paths containing spaces.

First use: open **Settings → Workspace**, register any additional disjoint folders, then configure an installed agent profile in **Settings**. Run its diagnostics and explicitly start/continue **Reverse engineer** until the complete documentation baseline covers the current workspace. Missing authentication, profile compatibility or confinement leaves setup visibly pending. The first portal startup initializes absent product state and attempts this bootstrap; it does not invent product verification or reset invalid existing state.

Write the change in **Current request**, Save draft, and submit **Clarify**. Repeat after reviewed answers/amendments until ready for **Analyze**, which generates the plan. Approve the identified plan, then explicitly **Implement**. Full required tests and documentation must pass before **Ready to close**; select **Close successfully** to archive. **Implement directly** records direct authority and generates its plan internally before changes.

Only one action can run. While starting, running, stopping, uncertain, or reserved for manual handoff, Stop is the only operational control; viewing/help/downloads remain available. No submissions are queued. A stopped blocked request remains open and permits independent read-only Q&A. [The user guide](USER_GUIDE.md#workflow) explains boundaries and recovery.

Useful commands:

```sh
python -B .aih/engine/cli.py status
python -B .aih/engine/cli.py operations
python -B .aih/engine/cli.py skills
python -B .aih/engine/cli.py doctor --wait
python -B .aih/engine/cli.py test
python -B .aih/engine/cli.py demo
```

Use `--help` for exact arguments and the [command reference](USER_GUIDE.md#commands). Install a pinned local core with `python -B /path/to/source/.aih/engine/cli.py install --source /path/to/source/.aih --destination /path/to/product`. Existing product content is preserved. No automatic CLI installation, remote publication or Git initialization occurs.

Managed process execution currently requires a compatible Linux Landlock/seccomp host. Native Windows mutations/process execution fail closed where a safe backend is unavailable; use a compatible WSL2 distribution for operational execution. Windows launch wrappers and platform claims must be assessed separately from Linux tests. Authentication discovery is not evidence of a successful real-agent run. See [limitations and validation](USER_GUIDE.md#limitations) and the build's `logs/` evidence for actual tests.

For a hosting agent, optionally append this snippet to its existing instructions after human review; preserve existing content:

> When explicitly working through AIH, follow `.aih/run.md` at the registered framework home and the accepted action's current authority. Use deterministic helpers; do not edit the immutable core or human-owned instructions.

Read [the complete guide](USER_GUIDE.md), [installed skills](skills/README.md), and [authoritative conventions](conventions/README.md). Help works without initialization or agent authentication.
