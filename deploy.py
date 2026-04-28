import getpass
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def run(cmd, check=True, env=None):
    merged = os.environ.copy()
    if env:
        merged.update(env)
    print("$ " + " ".join(cmd))
    result = subprocess.run(cmd, cwd=ROOT, text=True, env=merged)
    if check and result.returncode != 0:
        raise SystemExit(result.returncode)
    return result.returncode

def request(method, url, token, data=None):
    body = None
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            content = res.read().decode("utf-8")
            return res.status, json.loads(content) if content else {}
    except urllib.error.HTTPError as exc:
        content = exc.read().decode("utf-8", "replace")
        try:
            payload = json.loads(content) if content else {}
        except json.JSONDecodeError:
            payload = {"message": content}
        return exc.code, payload

def ensure_repo(username, token, repo, overwrite):
    repo_url = f"https://api.github.com/repos/{username}/{repo}"
    status, payload = request("GET", repo_url, token)
    if status == 200:
        if not overwrite:
            raise SystemExit("Repository exists. Re-run and allow overwrite to push updates.")
        return payload
    if status != 404:
        raise SystemExit(f"GitHub lookup failed: {status} {payload}")
    status, payload = request("POST", "https://api.github.com/user/repos", token, {"name": repo, "private": False, "auto_init": False, "has_issues": True, "has_projects": False, "has_wiki": False})
    if status not in (200, 201):
        raise SystemExit(f"Repository creation failed: {status} {payload}")
    return payload

def configure_pages(username, token, repo):
    url = f"https://api.github.com/repos/{username}/{repo}/pages"
    status, payload = request("POST", url, token, {"build_type": "workflow"})
    if status in (200, 201, 204, 409):
        return
    print(f"Pages configuration response: {status} {payload}")

def maybe_claude():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return
    answer = input("Run Claude quality gate before deploy? [y/N]: ").strip().lower()
    if answer == "y":
        run([sys.executable, "tools/claude_quality_gate.py"], check=False)

def main():
    username = input("GitHub username: ").strip()
    if not username:
        raise SystemExit("GitHub username is required.")
    token = getpass.getpass("GitHub token: ").strip()
    if not token:
        raise SystemExit("GitHub token is required.")
    repo = input("Repository name [sytfix.com]: ").strip() or "sytfix.com"
    overwrite = input("Create if missing and overwrite existing main branch? [Y/n]: ").strip().lower() != "n"
    maybe_claude()
    ensure_repo(username, token, repo, overwrite)
    run(["git", "init"])
    run(["git", "checkout", "-B", "main"])
    run(["git", "config", "user.name", username], check=False)
    run(["git", "config", "user.email", f"{username}@users.noreply.github.com"], check=False)
    run(["git", "add", "-A"])
    committed = run(["git", "commit", "-m", "Deploy SytFix site"], check=False)
    if committed != 0:
        run(["git", "commit", "--allow-empty", "-m", "Deploy SytFix site"], check=False)
    run(["git", "remote", "remove", "origin"], check=False)
    safe_user = urllib.parse.quote(username, safe="")
    safe_token = urllib.parse.quote(token, safe="")
    authed_remote = f"https://{safe_user}:{safe_token}@github.com/{username}/{repo}.git"
    public_remote = f"https://github.com/{username}/{repo}.git"
    run(["git", "remote", "add", "origin", authed_remote])
    run(["git", "push", "-u", "origin", "main", "--force"], env={"GIT_TERMINAL_PROMPT": "0"})
    run(["git", "remote", "set-url", "origin", public_remote], check=False)
    configure_pages(username, token, repo)
    print(f"Repository: https://github.com/{username}/{repo}")
    print("GitHub Pages will build from the included workflow after the push finishes.")
    print("If using the custom domain, confirm DNS points sytfix.com to GitHub Pages and enforce HTTPS in repository settings.")

if __name__ == "__main__":
    main()
