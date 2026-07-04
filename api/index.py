"""Vercel Serverless entrypoint — ASGI adapter for FastAPI backend."""

import json
import asyncio
import sys
from pathlib import Path

_backend_root = Path(__file__).resolve().parent.parent / "backend"
if str(_backend_root) not in sys.path:
    sys.path.insert(0, str(_backend_root))

from app.main import app


async def handler(event: dict, _context: dict):
    body = event.get("body", "") or ""
    if event.get("isBase64Encoded", False):
        import base64
        body = base64.b64decode(body).decode("utf-8", errors="replace")

    http_method = event.get("httpMethod", "GET").upper()
    raw_query = event.get("rawQuery", "")
    headers_in = event.get("headers", {}) or {}

    scope: dict = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "method": http_method,
        "path": event.get("path", "/"),
        "raw_path": event.get("path", "/").encode(),
        "query_string": raw_query.encode(),
        "headers": [(k.lower().encode(), v.encode()) for k, v in headers_in.items()],
        "server": ("", 80),
        "client": ("", 0),
        "scheme": "https",
    }

    recv: asyncio.Queue[dict] = asyncio.Queue()
    await recv.put({"type": "http.request", "body": body.encode(), "more_body": False})

    status = [200]
    resp_headers: list[list[bytes]] = []
    resp_body: list[bytes] = []

    async def _recv():
        return await recv.get()

    async def _send(msg):
        if msg["type"] == "http.response.start":
            status[0] = msg["status"]
            resp_headers[:] = [[k.encode(), v.encode()] for k, v in msg.get("headers", [])]
        elif msg["type"] == "http.response.body":
            resp_body.append(msg.get("body", b""))

    try:
        await app(scope, _recv, _send)
    except Exception as exc:
        status[0] = 500
        resp_body[:] = [json.dumps({"error": str(exc)}).encode()]
        resp_headers[:] = [[b"content-type", b"application/json"]]

    headers_out = {}
    for k, v in resp_headers:
        headers_out[k.decode().lower()] = v.decode()

    return {
        "statusCode": status[0],
        "headers": headers_out,
        "body": b"".join(resp_body).decode(),
        "isBase64Encoded": False,
    }


def main(event, context):
    return asyncio.run(handler(event, context))
