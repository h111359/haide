#!/usr/bin/env python3
"""AIH's sole shared CLI/menu entry point. No shell templates or database required."""
from __future__ import annotations
import sys
sys.dont_write_bytecode = True
if sys.version_info < (3, 11):
    sys.stderr.write("AIH requires Python 3.11 or newer. Install a supported Python runtime and retry.\n")
    raise SystemExit(2)
import argparse
import json
import os
from pathlib import Path
import subprocess
from contextlib import contextmanager

from contracts import CORE, VERSION, Error, dumps, parse, sanitize


@contextmanager
def maintenance_admission(engine):
    """Synchronous test/demo admission; never initialize the user's product."""
    from storage import home_lock
    with home_lock(engine.home):
        if not engine.store.root.exists():
            yield
            return
        with engine.store.lock(timeout=0):
            from recovery import assert_recovery_available, _current
            assert_recovery_available(engine.store)
            state, _, _, _ = _current(engine.store, engine.home)
            if state is None:
                raise Error("maintenance-state", "Existing incomplete product state requires explicit recovery before tests or demonstrations.")
            if state.get("active_request"):
                raise Error("maintenance-busy", "Framework tests and demonstrations require no open request, including blocked or Ready to close requests. Close it deliberately before maintenance.")
            engine._load()
            engine._check_config()
            yield


def parser():
    from workflow import META
    p = argparse.ArgumentParser(description="AIH — a portable file-based AI product-development harness")
    p.add_argument("--home", help="Canonical home containing the sole installed .aih directory (independent of cwd)")
    p.add_argument("--version", action="version", version="AIH " + VERSION)
    commands = p.add_subparsers(dest="command", required=True)
    for command, description in (("init", "Idempotently initialize product state; preserve existing content"), ("status", "Read current state without starting work"), ("operations", "Typed operation/help catalog"), ("skills", "Read metadata-only skill discovery"), ("menu", "Shared interactive terminal menu"), ("test", "Run framework automated tests")):
        commands.add_parser(command, help=description, description=description)
    help_cmd = commands.add_parser("help", help="Read the maintained local user guide without initialization or an agent")
    help_cmd.add_argument("query", nargs="?", default="")
    serve = commands.add_parser("serve", help="Start the local portal, initializing and baselining on first startup")
    serve.add_argument("--port", type=int, default=8765)
    serve.add_argument("--no-browser", action="store_true", help="Print the URL; do not request a managed browser")
    install = commands.add_parser("install", help="Install a pinned local core without Git or network")
    install.add_argument("--source", required=True)
    install.add_argument("--destination", required=True)
    upgrade = commands.add_parser("upgrade", help="Upgrade from a pinned local core while idle with no open request")
    upgrade.add_argument("--source", required=True)
    demo = commands.add_parser("demo", help="Build and exercise explicitly synthetic end-to-end demonstration fixtures")
    demo.add_argument("--destination", help="An empty destination within the current writable workspace")
    artifact = commands.add_parser("artifact", help="Read an existing safe artifact")
    artifact.add_argument("path")
    worker = commands.add_parser("worker", help=argparse.SUPPRESS)
    worker.add_argument("operation_id")
    helper = commands.add_parser("helper", help="Read-only deterministic substep of an already accepted action")
    from helpers import OPERATIONS
    helper.add_argument("operation", choices=list(OPERATIONS) + ["catalog"])
    helper.add_argument("--owner", help="Current accepted operational owner ID")
    helper.add_argument("--payload", default="{}", help="Typed JSON helper inputs")
    run = commands.add_parser("run", help="Invoke a typed operation; no arbitrary shell command accepted")
    run.add_argument("operation", choices=list(META))
    def inputs(cmd):
        group = cmd.add_mutually_exclusive_group()
        group.add_argument("--payload", default=None, help="JSON object containing typed inputs")
        group.add_argument("--payload-file", help="Explicit UTF-8 JSON input file (screened before retention)")
        cmd.add_argument("--expected-revision", type=int)
        cmd.add_argument("--idempotency-key", help="Stable key for retries of the identical accepted action")
        cmd.add_argument("--wait", action="store_true", help="Run this action in the foreground and wait for its result")
    inputs(run)
    for name, metadata in META.items():
        cmd = commands.add_parser(name, help=metadata[1], description=metadata[1] + " Required payload fields: " + (", ".join(metadata[2]) or "none"))
        inputs(cmd)
    return p


def menu(home=None):
    from workflow import Engine
    engine = Engine(home)
    while True:
        status = engine.status()
        print("\nAIH " + VERSION + " · " + str(engine.home))
        print("Status: " + ("busy — Stop is the only operational control" if status.get("busy") else "idle") + "; setup: " + status.get("setup", {}).get("status", "unknown"))
        for root in status.get("config", {}).get("workspace", {}).get("roots", []):
            print(f"  {root['id']}: {root['path']} ({root['access']})")
        if status.get("busy"):
            choices = {"1": "Show current status", "2": "Stop execution", "3": "Open help", "0": "Exit"}
        else:
            choices = {"1": "Open portal", "2": "Show current status", "3": "Configure/check agent profiles", "4": "Workspace settings", "5": "Initialization/reverse engineering", "6": "Validate framework/product state", "7": "Inspect/resume interrupted operations", "8": "Open help", "0": "Exit"}
        for key, label in choices.items():
            print(key + ". " + label)
        try:
            choice = input("Select: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nMenu closed. Existing workers and requests were not cancelled.")
            return
        if choice == "0":
            print("Existing workers and requests remain unchanged."); return
        label = choices.get(choice)
        try:
            if label == "Open portal":
                # Independent portal process; closing the menu never cancels an accepted action.
                command = [sys.executable, "-B", str(CORE / "engine/cli.py"), "--home", str(engine.home), "serve", "--no-browser"]
                process = subprocess.Popen(command, cwd=engine.home, stdin=subprocess.DEVNULL, start_new_session=os.name == "posix")
                print("Portal starting or reusing http://127.0.0.1:8765 (process " + str(process.pid) + ").")
            elif label == "Show current status":
                print(dumps(engine.status()))
            elif label == "Open help":
                print((CORE / "USER_GUIDE.md").read_text("utf-8"))
            elif label == "Stop execution":
                print(dumps(engine.dispatch("stop")))
            elif label == "Initialization/reverse engineering":
                engine.initialize()
                print(dumps(engine.dispatch("reverse-engineer")))
            elif label == "Validate framework/product state":
                print(dumps(engine.dispatch("validate")))
            elif label == "Configure/check agent profiles":
                if engine.initialized():
                    print(dumps(engine.dispatch("doctor")))
                print("Configure deliberately in Settings → Agent profiles, or profile-save --payload-file profile.json.")
            elif label == "Workspace settings":
                print(dumps(status.get("config", {}).get("workspace", {})))
                print("Use Settings → Workspace or workspace-save --payload-file roots.json. Saving never starts an agent.")
            elif label == "Inspect/resume interrupted operations":
                print(dumps(status.get("runs", [])))
                print("To explicitly continue an identified stopped action: resume --payload '{\"operation_id\":\"OP-ID\"}'.")
            else:
                print("Select one of the listed choices.")
        except Exception as exc:
            print("Action could not complete: " + sanitize(str(exc)))


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == "help":
            text = (CORE / "USER_GUIDE.md").read_text("utf-8")
            if args.query:
                paragraphs = text.split("\n\n")
                text = "\n\n".join(p for p in paragraphs if args.query.casefold() in p.casefold()) or "No matching guide text. Run help without a query for the full guide."
            print(text); return 0
        if args.command == "operations":
            from workflow import catalog
            print(dumps({"version": VERSION, "operations": catalog()})); return 0
        if args.command == "install":
            from installation import install
            print(dumps(install(args.source, args.destination))); return 0
        from workflow import Engine
        engine = Engine(args.home)
        if args.command == "init":
            result = engine.initialize()
        elif args.command == "status":
            result = engine.status()
        elif args.command == "skills":
            if engine.initialized():
                engine._load()
            result = {"skills": engine.skills()}
        elif args.command == "serve":
            from portal import run_server
            run_server(engine.home, port=args.port, no_browser=args.no_browser)
            return 0
        elif args.command == "menu":
            menu(engine.home); return 0
        elif args.command == "worker":
            engine.worker(args.operation_id); return 0
        elif args.command == "helper":
            from helpers import invoke, OPERATIONS
            result = {"helpers": OPERATIONS} if args.operation == "catalog" else invoke(engine, args.operation, args.owner, parse(args.payload))
        elif args.command == "artifact":
            result = engine.artifact(args.path)
        elif args.command == "upgrade":
            from installation import upgrade
            result = upgrade(engine.home, args.source)
        elif args.command == "test":
            with maintenance_admission(engine):
                if engine.home != CORE.parent.resolve():
                    raise Error("self-test-home", "Run the selected home's installed .aih/engine/cli.py test command so test fixtures remain in that registered home.")
                import unittest
                root = engine.home / ".aih_runtime/self-test"
                root.mkdir(parents=True, exist_ok=True)
                import tempfile
                previous_temp = tempfile.tempdir
                try:
                    tempfile.tempdir = str(root)
                    tests = unittest.defaultTestLoader.discover(str(CORE / "engine/tests"))
                    outcome = unittest.TextTestRunner(verbosity=2).run(tests)
                finally:
                    tempfile.tempdir = previous_temp
                return 0 if outcome.wasSuccessful() else 1
        elif args.command == "demo":
            with maintenance_admission(engine):
                from demo import demonstrate
                result = demonstrate(engine.home, args.destination)
        else:
            if args.payload_file:
                path = Path(args.payload_file)
                if path.stat().st_size > 1024 * 1024:
                    raise Error("input-size", "Typed payload files must be at most 1 MiB.")
                payload = parse(path.read_text("utf-8"), "operation payload")
            else:
                payload = parse(args.payload or "{}", "operation payload")
            result = engine.dispatch(args.operation if args.command == "run" else args.command, payload, args.expected_revision, args.idempotency_key, background=not args.wait)
        print(dumps(result))
        return 0 if result.get("ok", True) and result.get("status") not in ("blocked", "failed", "uncertain") else 2
    except Exception as exc:
        if isinstance(exc, Error):
            result = exc.result()
        else:
            result = {"ok": False, "error": {"code": getattr(exc, "code", "operation-failed"), "message": sanitize(str(exc)), "details": getattr(exc, "details", {})}}
        print(dumps(result), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
