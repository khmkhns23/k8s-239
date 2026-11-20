import html
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer


class ApiHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # รองรับทั้ง /api/<ข้อความ> และ /<ข้อความ>
        if path.startswith("/api/"):
            raw_msg = path[len("/api/"):]
        elif path == "/api":
            raw_msg = "กรุณาพิมพ์ข้อความต่อท้าย เช่น /api/Hello"
        else:
            raw_msg = path.lstrip("/") or "กรุณาพิมพ์ข้อความต่อท้าย เช่น /api/Hello"

        message = urllib.parse.unquote(raw_msg)
        safe_msg = html.escape(message)

        body = f"""<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>API Display - {safe_msg}</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      background: linear-gradient(135deg, #e0f2fe 0%, #ede9fe 50%, #fce7f3 100%);
      color: #0f172a;
      font-family: 'Segoe UI', Tahoma, sans-serif;
    }}
    .navbar {{
      background: rgba(255, 255, 255, 0.88);
      backdrop-filter: blur(8px);
      border-bottom: 1px solid #e2e8f0;
      padding: 14px 28px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .brand {{ font-weight: 800; font-size: 1.1rem; color: #be185d; }}
    .nav-links {{ display: flex; gap: 18px; flex-wrap: wrap; }}
    .nav-links a {{ text-decoration: none; color: #475569; font-weight: 600; font-size: 0.95rem; }}
    .nav-links a:hover, .nav-links a.active {{ color: #be185d; }}
    .center-stage {{
      flex: 1;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 32px 20px;
    }}
    .display-card {{
      background: rgba(255, 255, 255, 0.92);
      border: 1px solid #ffffff;
      border-radius: 28px;
      padding: 56px 48px;
      max-width: 90vw;
      text-align: center;
      box-shadow: 0 24px 60px rgba(190, 24, 93, 0.12);
    }}
    .api-badge {{
      display: inline-block;
      background: #fce7f3;
      color: #be185d;
      padding: 6px 16px;
      border-radius: 999px;
      font-size: 0.85rem;
      font-weight: 700;
      margin-bottom: 20px;
    }}
    .big-text {{
      font-size: clamp(2.8rem, 8vw, 6.2rem);
      font-weight: 900;
      line-height: 1.15;
      background: linear-gradient(135deg, #2563eb 0%, #7c3aed 50%, #db2777 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      word-break: break-word;
    }}
    .sub {{
      margin-top: 24px;
      color: #64748b;
      font-size: 0.95rem;
    }}
  </style>
</head>
<body>
  <nav class="navbar">
    <div class="brand">K8s Ingress Portal &bull; id-239</div>
    <div class="nav-links">
      <a href="/">หน้าแรก</a>
      <a href="/about">About</a>
      <a href="/research">Research</a>
      <a class="active" href="/api/Hello%2068130239">API</a>
      <a href="http://admin.id-239.com">Admin</a>
    </div>
  </nav>

  <main class="center-stage">
    <div class="display-card">
      <div class="api-badge">Service: app-api</div>
      <div class="big-text">{safe_msg}</div>
      <div class="sub">Yutthasatr Khumkhonsue &bull; ID: 68130239</div>
    </div>
  </main>
</body>
</html>"""
        data = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8080), ApiHandler)
    print("app-api listening on port 8080...")
    server.serve_forever()
