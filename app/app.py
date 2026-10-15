from datetime import datetime, timezone
from html import escape
import os
import socket

from flask import Flask, jsonify

app = Flask(__name__)

ENV_NAME = os.getenv("ENV_NAME", "local")
HOSTNAME = socket.gethostname()

INDEX_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>test-app</title>
  <style>
    body {{ font-family: system-ui, sans-serif; background: #f4f6f8; color: #1f2933;
           display: flex; justify-content: center; padding: 48px 16px; margin: 0; }}
    .card {{ background: #fff; border-radius: 12px; padding: 32px; max-width: 480px; width: 100%;
             box-shadow: 0 2px 12px rgba(0, 0, 0, .08); }}
    h1 {{ margin: 0 0 8px; font-size: 24px; }}
    .ok {{ color: #1a7f37; font-weight: 600; }}
    table {{ width: 100%; border-collapse: collapse; margin: 24px 0; }}
    td {{ padding: 8px 0; border-bottom: 1px solid #e4e7eb; }}
    td:first-child {{ color: #616e7c; width: 40%; }}
    code {{ background: #f0f2f5; padding: 2px 6px; border-radius: 4px; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>test-app</h1>
    <div class="ok">&#9679; Status: ok</div>
    <table>
      <tr><td>Environment</td><td><code>{env}</code></td></tr>
      <tr><td>Served by (pod)</td><td><code>{host}</code></td></tr>
      <tr><td>Server time (UTC)</td><td>{time}</td></tr>
    </table>
    <a href="/healthz">/healthz</a> &mdash; JSON health check
  </div>
</body>
</html>
"""


@app.route("/")
def index():
    return INDEX_HTML.format(
        env=escape(ENV_NAME),
        host=escape(HOSTNAME),
        time=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
    )


@app.route("/healthz")
def health():
    return jsonify({
        "status": "ok",
        "service": "app",
        "env": ENV_NAME
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080
    )
