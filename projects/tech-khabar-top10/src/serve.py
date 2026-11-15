#!/usr/bin/env python3
"""Tiny static server with HTTP Range support (needed for <video> seeking).
Serves the project folder; '/' is a player page."""
import os, re, sys, mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
PORT = int(os.environ.get("PORT", sys.argv[2] if len(sys.argv) > 2 else 8000))

INDEX = """<!doctype html><meta charset="utf-8">
<title>Tech Khabar — Top 10 (14 Nov 2026)</title>
<style>
body{margin:0;background:#12100e;color:#f5ece2;font:16px/1.5 system-ui,sans-serif;
display:flex;flex-direction:column;align-items:center;gap:14px;padding:22px}
h1{font-size:18px;font-weight:600;letter-spacing:.02em;margin:0}
h1 span{color:#d97757}
video{width:min(100%,1100px);border-radius:10px;background:#000;box-shadow:0 18px 40px rgba(0,0,0,.5)}
a{color:#e5b09a}ul{list-style:none;padding:0;margin:0;font-size:14px;opacity:.85;text-align:center}
li{display:inline-block;margin:0 8px}
</style>
<h1>TECH<span>KHABAR</span> · Top 10 — 14 Nov 2026 · 1920x1080 · 2:46</h1>
<video controls preload="metadata" playsinline
  src="./export/tech-khabar-top10.mp4"></video>
<ul>
<li><a href="./export/tech-khabar-top10.mp4" download>download mp4 (31 MB)</a></li>
<li><a href="./review/final_sheet.jpg">all 14 scenes</a></li>
<li><a href="./review/cover.jpg">cover frame</a></li>
<li><a href="./caption.md">caption</a></li>
</ul>
"""


class H(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):
        pass

    def do_HEAD(self):
        self.serve(head=True)

    def do_GET(self):
        self.serve(head=False)

    def serve(self, head=False):
        path = self.path.split("?")[0]
        if path == "/":
            body = INDEX.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            if not head:
                self.wfile.write(body)
            return

        rel = os.path.normpath(os.path.join(ROOT, path.lstrip("/")))
        if not rel.startswith(ROOT) or not os.path.isfile(rel):
            self.send_error(404)
            return

        size = os.path.getsize(rel)
        ctype = mimetypes.guess_type(rel)[0] or "application/octet-stream"
        if rel.endswith(".md"):
            ctype = "text/plain; charset=utf-8"

        rng = self.headers.get("Range")
        start, end = 0, size - 1
        status = 200
        if rng:
            m = re.match(r"bytes=(\d*)-(\d*)", rng)
            if m:
                a, b = m.group(1), m.group(2)
                if a:
                    start = int(a)
                    if b:
                        end = min(int(b), size - 1)
                elif b:
                    start = max(size - int(b), 0)
                status = 206

        length = end - start + 1
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(length))
        if status == 206:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.end_headers()
        if head:
            return
        with open(rel, "rb") as f:
            f.seek(start)
            left = length
            while left > 0:
                chunk = f.read(min(262144, left))
                if not chunk:
                    break
                self.wfile.write(chunk)
                left -= len(chunk)


ThreadingHTTPServer(("0.0.0.0", PORT), H).serve_forever()
