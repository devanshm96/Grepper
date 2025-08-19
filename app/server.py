from flask import Flask, request, jsonify, render_template_string
from app.grep_core import grep_match

app = Flask(__name__)

INDEX_HTML = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Mini Grep UI</title>
    <style>
      body { font-family: system-ui, sans-serif; margin: 2rem; max-width: 800px; }
      textarea, input { width: 100%; box-sizing: border-box; margin: 0.25rem 0; }
      .btn { padding: 0.5rem 0.75rem; margin-top: 0.5rem; }
      pre { background: #f6f8fa; padding: 1rem; border-radius: 6px; }
      .muted { color: #666; }
    </style>
  </head>
  <body>
    <h1>Grep (custom)</h1>
    <label>Pattern</label>
    <input id="pattern" placeholder="\\d, \\w, [abc], [^xyz], or single char" />
    <label>Text</label>
    <textarea id="text" rows="10" placeholder="Paste text here..."></textarea>
    <button class="btn" id="run">Run</button>
    <p class="muted">Note: This demo supports a limited subset: \\d, \\w, [..], [^..], and single-char.</p>
    <h3>Matches</h3>
    <pre id="output"></pre>
    <script>
      document.getElementById('run').addEventListener('click', async () => {
        const pattern = document.getElementById('pattern').value;
        const text = document.getElementById('text').value;
        const res = await fetch('/grep', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ pattern, text })
        });
        const data = await res.json();
        document.getElementById('output').textContent = data.matches.join('\\n');
      });
    </script>
  </body>
</html>
"""

@app.get("/")
def index():
    return render_template_string(INDEX_HTML)

@app.post("/grep")
def grep():
    payload = request.get_json(force=True)
    pattern = payload.get("pattern", "")
    text = payload.get("text", "")
    try:
        matches = grep_match(text, pattern)
        return jsonify({"matches": matches})
    except Exception as e:
        return jsonify({"error": str(e), "matches": []}), 400

if __name__ == "__main__":
    # For local run
    app.run(host="0.0.0.0", port=8000)