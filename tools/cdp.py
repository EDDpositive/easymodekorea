"""Tiny driver for a headless Edge or Chrome, standard library only.

Used by the store screenshots and the browser checks. It opens the browser with a throwaway
profile, sets a phone-sized screen, and lets a script load pages, run JavaScript and take
screenshots through the browser's debugging port.
"""
import base64, json, os, shutil, socket, struct, subprocess, tempfile, time, urllib.parse, urllib.request

BROWSERS = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "/usr/bin/google-chrome", "/usr/bin/chromium-browser", "/usr/bin/chromium"]


def find_browser():
    for b in [os.environ.get("EMK_BROWSER", "")] + BROWSERS:
        if b and os.path.exists(b): return b
    raise SystemExit("No Edge or Chrome found (set EMK_BROWSER to its path).")


class _Socket:
    """Just enough WebSocket to talk to the debugging port: text frames, client masking."""
    def __init__(self, url):
        u = urllib.parse.urlparse(url)
        self.s = socket.create_connection((u.hostname, u.port), timeout=60)
        key = base64.b64encode(os.urandom(16)).decode()
        self.s.sendall(f"GET {u.path} HTTP/1.1\r\nHost: {u.hostname}:{u.port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n".encode())
        buf = b""
        while b"\r\n\r\n" not in buf: buf += self.s.recv(4096)
        self.buf = buf.split(b"\r\n\r\n", 1)[1]

    def send(self, text):
        data = text.encode(); n = len(data); mask = os.urandom(4)
        head = bytes([0x80 | n]) if n < 126 else bytes([0x80 | 126]) + struct.pack(">H", n) if n < 65536 else bytes([0x80 | 127]) + struct.pack(">Q", n)
        self.s.sendall(b"\x81" + head + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(data)))

    def _read(self, n):
        while len(self.buf) < n:
            chunk = self.s.recv(1 << 16)
            if not chunk: raise EOFError("browser closed the connection")
            self.buf += chunk
        out, self.buf = self.buf[:n], self.buf[n:]
        return out

    def recv(self):
        msg = b""
        while True:
            b1, b2 = self._read(2); n = b2 & 0x7F
            if n == 126: n = struct.unpack(">H", self._read(2))[0]
            elif n == 127: n = struct.unpack(">Q", self._read(8))[0]
            data = self._read(n); op = b1 & 0x0F
            if op == 8: raise EOFError("browser closed the connection")
            if op in (9, 10): continue
            msg += data
            if b1 & 0x80: return msg.decode("utf-8", "replace")


class Browser:
    def __init__(self, width=360, height=640, scale=3, scheme="light", port=9377):
        extra = ["--no-sandbox"] if os.environ.get("CI") else []  # hosted CI runners cannot start the browser sandbox
        target = None; self.proc = None; self.profile = None
        for attempt in range(3):  # a busy CI runner sometimes fails to bring the browser up; a fresh try fixes it
            self.profile = tempfile.mkdtemp(prefix="emk-cdp-")
            self.proc = subprocess.Popen([find_browser(), "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check", "--hide-scrollbars", *extra,
                                          f"--remote-debugging-port={port + attempt}", "--remote-allow-origins=*", f"--user-data-dir={self.profile}", "about:blank"],
                                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            for _ in range(150):
                try:
                    pages = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port + attempt}/json/list", timeout=2))
                    target = next((p for p in pages if p.get("type") == "page"), None)
                    if target: break
                except OSError: pass
                time.sleep(0.2)
            if target: break
            self.proc.kill(); self.proc.wait(); shutil.rmtree(self.profile, ignore_errors=True)
        if not target: raise SystemExit("The browser did not start.")
        self.ws = _Socket(target["webSocketDebuggerUrl"]); self.id = 0; self.events = []
        for m in ("Page.enable", "Runtime.enable"): self.cmd(m)
        self.cmd("Emulation.setDeviceMetricsOverride", width=width, height=height, deviceScaleFactor=scale, mobile=True)
        self.cmd("Emulation.setTouchEmulationEnabled", enabled=True)
        self.media(scheme)

    def cmd(self, method, **params):
        self.id += 1; self.ws.send(json.dumps({"id": self.id, "method": method, "params": params}))
        while True:
            m = json.loads(self.ws.recv())
            if m.get("id") == self.id:
                if "error" in m: raise RuntimeError(f"{method}: {m['error']}")
                return m.get("result", {})
            self.events.append(m)

    def media(self, scheme="light"):
        self.cmd("Emulation.setEmulatedMedia", features=[{"name": "prefers-color-scheme", "value": scheme}])

    def go(self, url, wait=1.2):
        """Load a page and give fonts and scripts a moment. Returns False when the page fails to load at all."""
        r = self.cmd("Page.navigate", url=url)
        if r.get("errorText"): return False
        end = time.time() + 20
        while time.time() < end:
            if self.js("document.readyState") == "complete": break
            time.sleep(0.1)
        time.sleep(wait)
        return True

    def js(self, expr):
        r = self.cmd("Runtime.evaluate", expression=expr, awaitPromise=True, returnByValue=True)
        if "exceptionDetails" in r: raise RuntimeError(r["exceptionDetails"].get("exception", {}).get("description", "script error"))
        return r["result"].get("value")

    def shot(self, path):
        data = self.cmd("Page.captureScreenshot", format="png")["data"]
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        open(path, "wb").write(base64.b64decode(data))

    def close(self):
        try: self.cmd("Browser.close")
        except Exception: pass
        try: self.proc.wait(timeout=10)
        except Exception: self.proc.kill()
        shutil.rmtree(self.profile, ignore_errors=True)


class Server:
    """Serves the repo root on localhost, so checks and screenshots need no other setup."""
    def __init__(self, root, port=8791):
        import sys
        self.url = f"http://localhost:{port}/"
        self.proc = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1", "-d", root], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(50):
            try: urllib.request.urlopen(self.url + "manifest.webmanifest", timeout=2); return
            except OSError: time.sleep(0.2)
        raise SystemExit("The local server did not start.")

    def stop(self):
        self.proc.kill(); self.proc.wait()
