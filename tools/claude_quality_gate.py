import json
import os
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KEY = os.environ.get("ANTHROPIC_API_KEY")

def collect():
    parts = []
    for pattern in ("*.html", "assets/css/*.css", "assets/js/*.js"):
        for path in sorted(ROOT.glob(pattern)):
            parts.append(f"\n\nFILE: {path.relative_to(ROOT)}\n{path.read_text(encoding='utf-8')[:24000]}")
    return "".join(parts)[:140000]

def main():
    if not KEY:
        print("ANTHROPIC_API_KEY is not set. Skipping Claude quality gate.")
        return
    prompt = "Review this static website for mobile layout risks, SEO metadata quality, link clarity, conversion friction, accessibility, and visual consistency. Return JSON with pass, risks, and fixes. Do not rewrite the site.\n" + collect()
    data = {
        "model": os.environ.get("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest"),
        "max_tokens": 3000,
        "messages": [{"role": "user", "content": prompt}]
    }
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(data).encode("utf-8"),
        method="POST",
        headers={
            "content-type": "application/json",
            "x-api-key": KEY,
            "anthropic-version": "2023-06-01"
        }
    )
    with urllib.request.urlopen(req, timeout=90) as res:
        payload = json.loads(res.read().decode("utf-8"))
    out = ROOT / "build" / "claude-quality-report.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {out.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
