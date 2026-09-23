"""Loopback-only local portal using the same typed Engine operations as the CLI.

No arbitrary command endpoint, uncontrolled browser launch, or external assets.
Each HTTP request obtains its own Engine facade; file transactions own concurrency.
"""
from __future__ import annotations

import hmac
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
from pathlib import Path
import secrets
import threading
import urllib.error
import urllib.parse
import urllib.request

from contracts import Error, VERSION, parse, screen
from storage import sanitize
from workflow import Engine

MAX_BODY = 1024 * 1024
ASSETS = {"/": "index.html", "/index.html": "index.html", "/app.css": "app.css", "/app.js": "app.js"}


def _error(exc):
    if hasattr(exc, "result"):
        return sanitize(exc.result())
    if hasattr(exc, "code"):
        return sanitize({"ok": False, "error": {"code": exc.code, "message": str(exc), "details": getattr(exc, "details", {})}})
    return {"ok": False, "error": {"code": "portal-error", "message": "The local operation could not finish. Inspect framework diagnostics; no raw exception or credential is exposed."}}


def _error_status(exc):
    code = getattr(exc, "code", "")
    if "conflict" in code or code == "busy":
        return 409
    if code in ("not-found", "artifact-missing") or isinstance(exc, FileNotFoundError):
        return 404
    if any(word in code for word in ("boundary", "origin", "csrf", "host", "authority", "permission", "escape")):
        return 403
    return 400


class PortalServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, home, port=8765, *, engine_factory=None):
        self.home = Path(home).resolve()
        self.engine_factory = engine_factory or (lambda: Engine(self.home))
        self.csrf_token = secrets.token_urlsafe(32)
        self.setup_error = None
        self.bootstrap_thread = None
        super().__init__(("127.0.0.1", port), PortalHandler)
        self.port = self.server_address[1]
        self.url = f"http://127.0.0.1:{self.port}"

    def bootstrap(self):
        """Automatic first-start setup outside HTTP handlers; engine deduplicates ownership."""
        try:
            engine = self.engine_factory()
            result = engine.initialize()
            if not result.get("reused", False):
                engine.dispatch("reverse-engineer", {"mode": "initial"},
                                expected_revision=result.get("revision"),
                                idempotency_key="portal-initial-baseline", human=True, background=True)
        except Exception as exc:
            self.setup_error = _error(exc)

    def start_bootstrap(self):
        self.bootstrap_thread = threading.Thread(target=self.bootstrap, name="aih-portal-bootstrap", daemon=True)
        self.bootstrap_thread.start()


class PortalHandler(BaseHTTPRequestHandler):
    server_version = "AIH/" + VERSION
    sys_version = ""
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        # URLs, content and request headers must never become unreviewed logs.
        pass

    def _host(self):
        raw = self.headers.get("Host", "")
        accepted = {f"127.0.0.1:{self.server.port}", f"localhost:{self.server.port}"}
        if self.server.port == 80:
            accepted |= {"127.0.0.1", "localhost"}
        if raw not in accepted:
            raise Error("invalid-host", "Use the exact loopback portal URL printed by the launcher.")
        return raw

    def _same_origin(self):
        host = self._host()
        if self.headers.get("Origin") != "http://" + host:
            raise Error("invalid-origin", "State-changing requests require this portal's exact local origin.")
        if self.headers.get("Sec-Fetch-Site", "same-origin") not in ("same-origin", "none"):
            raise Error("invalid-origin", "Cross-site portal operations are prohibited.")
        if not hmac.compare_digest(self.headers.get("X-AIH-Token", ""), self.server.csrf_token):
            raise Error("invalid-csrf", "Reload this portal to obtain its current request token.")

    def _send(self, body, status=200, content_type="application/json; charset=utf-8", *, filename=None):
        if not isinstance(body, bytes):
            body = (json.dumps(body, ensure_ascii=False, allow_nan=False) if not isinstance(body, str) else body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; font-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'")
        if filename:
            safe = "".join(c for c in Path(filename).name if c.isascii() and (c.isalnum() or c in "._-")) or "artifact.txt"
            self.send_header("Content-Disposition", 'attachment; filename="' + safe + '"')
        self.end_headers()
        if self.command != "HEAD":
            try:
                self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError):
                pass

    def _fail(self, exc):
        self.close_connection = True
        self._send(_error(exc), _error_status(exc))

    def do_GET(self):
        try:
            self._host()
            url = urllib.parse.urlsplit(self.path)
            if url.path in ASSETS:
                path = Path(__file__).parent / "ui" / ASSETS[url.path]
                content_type = {".html": "text/html", ".css": "text/css", ".js": "text/javascript"}[path.suffix]
                return self._send(path.read_bytes(), content_type=content_type + "; charset=utf-8")
            if url.path == "/api/help":
                core = self.server.home / ".aih"
                return self._send({"markdown": (core / "USER_GUIDE.md").read_text(encoding="utf-8"), "quick_start": (core / "README.md").read_text(encoding="utf-8"), "version": VERSION})
            engine = self.server.engine_factory()
            if url.path == "/api/status":
                try:
                    state = engine.status()
                except Exception as exc:
                    if self.server.bootstrap_thread and self.server.bootstrap_thread.is_alive():
                        state = {"revision": 0, "product": {"name": self.server.home.name, "home": str(self.server.home)}, "busy": True, "setup": {"status": "initializing", "message": "Initializing safe deterministic product files."}}
                    else:
                        raise exc
                state = sanitize(state)
                state["csrf_token"] = self.server.csrf_token
                state["home"] = str(self.server.home)
                state.setdefault("version", VERSION)
                if self.server.setup_error:
                    state["portal_setup_diagnostic"] = self.server.setup_error
                return self._send(state)
            if url.path == "/api/catalog":
                return self._send({"operations": sanitize(engine.operations()), "portal_actions": json.loads((Path(__file__).parent / "ui/actions.json").read_text(encoding="utf-8")), "version": VERSION})
            if url.path == "/api/artifacts":
                args = urllib.parse.parse_qs(url.query, strict_parsing=True)
                refs = args.get("path", [])
                if len(refs) != 1 or not refs[0]:
                    raise Error("invalid-reference", "Provide one stored artifact reference.")
                result = engine.artifact(refs[0])
                if isinstance(result, dict):
                    text = result.get("content", result.get("text", json.dumps(result, ensure_ascii=False)))
                else:
                    text = result.decode("utf-8") if isinstance(result, bytes) else str(result)
                return self._send(sanitize(text), content_type="text/plain; charset=utf-8", filename=refs[0] if args.get("download") == ["1"] else None)
            raise Error("not-found", "This local portal resource is unavailable.")
        except Exception as exc:
            self._fail(exc)

    def do_HEAD(self):
        self.do_GET()

    def do_POST(self):
        try:
            self._same_origin()
            if urllib.parse.urlsplit(self.path).path != "/api/operation":
                raise Error("not-found", "Only catalogued typed operations are accepted.")
            if self.headers.get_content_type() != "application/json":
                raise Error("invalid-content-type", "Provide an application/json operation object.")
            if self.headers.get("Transfer-Encoding"):
                raise Error("invalid-body", "Chunked operation intake is not supported.")
            raw_length = self.headers.get("Content-Length", "")
            if not raw_length.isdecimal() or not 0 < int(raw_length) <= MAX_BODY:
                raise Error("input-size", "Operation intake requires a bounded JSON body of at most 1 MiB.")
            body = self.rfile.read(int(raw_length)).decode("utf-8")
            request = parse(body, "operation request")
            if not isinstance(request, dict) or set(request) - {"operation", "expected_revision", "idempotency_key", "payload"}:
                raise Error("invalid-operation", "Use the documented typed operation envelope.")
            if not isinstance(request.get("operation"), str) or not isinstance(request.get("payload", {}), dict):
                raise Error("invalid-operation", "Operation must be an ID and payload must be an object.")
            if type(request.get("expected_revision")) is not int or not isinstance(request.get("idempotency_key"), str):
                raise Error("revision-required", "Operational requests require a state revision and idempotency key.")
            if request["operation"] != "redact":
                screen(body, "portal intake")
            result = self.server.engine_factory().dispatch(
                request["operation"], request.get("payload", {}),
                expected_revision=request["expected_revision"],
                idempotency_key=request["idempotency_key"], human=True, background=True)
            self._send(sanitize(result))
        except (UnicodeError, ValueError) as exc:
            if hasattr(exc, "code"):
                self._fail(exc)
            else:
                self._fail(Error("invalid-input", "Provide valid bounded UTF-8 JSON; rejected intake was not saved."))
        except Exception as exc:
            self._fail(exc)

    def do_OPTIONS(self):
        self._send({"ok": False, "error": {"code": "cross-origin", "message": "Cross-origin access is not supported."}}, 403)


def existing_portal(home, port):
    """Read existing loopback metadata; never treat an unrelated service as AIH."""
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/status", timeout=1) as response:
            status = json.load(response)
        actual = status.get("home") or status.get("product", {}).get("home")
        if actual and Path(actual).resolve() == Path(home).resolve() and "csrf_token" in status:
            return f"http://127.0.0.1:{port}"
    except (OSError, ValueError, urllib.error.URLError):
        pass
    return None


def run_server(home, port=8765, no_browser=True):
    """Serve until interrupted; stopping the portal alone never cancels owned work."""
    try:
        server = PortalServer(home, int(port))
    except OSError as exc:
        existing = existing_portal(home, int(port))
        if existing:
            print(f"AIH portal is already serving this product: {existing}", flush=True)
            return {"ok": True, "reused": True, "url": existing}
        raise Error("port-in-use", f"Port {port} is unavailable. Use --port with another local port.") from exc
    server.start_bootstrap()
    print(f"AIH portal: {server.url}", flush=True)
    if not no_browser:
        print("Open this URL in your browser. Automatic browser launch is disabled because this installation has not configured a confined managed browser profile and caches.", flush=True)
    try:
        server.serve_forever(poll_interval=.2)
    except KeyboardInterrupt:
        print("Portal stopped. Existing execution ownership remains recorded; use explicit Stop to cancel work.", flush=True)
    finally:
        server.server_close()
    return {"ok": True, "url": server.url, "status": "portal-stopped"}
