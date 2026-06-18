#!/usr/bin/env python3
"""
SytFix Deployment Script
=========================
Zips the website directory and pushes it to a GitHub repository using a
personal access token. Pushing to the connected GitHub repo triggers an
automatic Vercel deployment if the repo is linked to a Vercel project.

USAGE
-----
    python deploy.py

You will be prompted for your GitHub Personal Access Token (PAT) at runtime.
The token is never written to disk or echoed to the terminal.

Alternatively, set the GITHUB_TOKEN environment variable beforehand to skip
the prompt:

    Windows (PowerShell):  $env:GITHUB_TOKEN = "ghp_xxxxxxxxxxxx"
    macOS / Linux:         export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"

CONFIGURATION
-------------
Edit the CONFIG block below before first use. At minimum, set:
    - GITHUB_USERNAME
    - GITHUB_REPO
    - BRANCH (defaults to "main")

REQUIREMENTS
------------
    pip install requests --break-system-packages   (if not already installed)
    Git must be installed and available on PATH.
"""

import os
import sys
import zipfile
import getpass
import subprocess
import shutil
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("The 'requests' library is required. Install it with:")
    print("    pip install requests --break-system-packages")
    sys.exit(1)


# ============================================================
# CONFIGURATION — edit these before running
# ============================================================
GITHUB_USERNAME = "RAMitchell4"          # your GitHub username
GITHUB_REPO     = "sytfix"               # repo name (without .git)
BRANCH          = "main"                 # branch to push to
COMMIT_MESSAGE  = None                   # None = auto-generate timestamped message

SITE_DIR        = Path(__file__).resolve().parent   # directory containing this script
ZIP_OUTPUT_DIR  = SITE_DIR / "_deploy_archive"
EXCLUDE_DIRS    = {".git", "_deploy_archive", "__pycache__", "node_modules"}
EXCLUDE_FILES   = {".DS_Store"}


# ============================================================
# HELPERS
# ============================================================
def log(msg, level="INFO"):
    prefix = {"INFO": "→", "OK": "✓", "WARN": "!", "ERR": "✗"}.get(level, "→")
    print(f"  {prefix}  {msg}")


def confirm(prompt):
    answer = input(f"{prompt} [y/N]: ").strip().lower()
    return answer in ("y", "yes")


def get_token():
    """Read the GitHub PAT from environment, or prompt securely."""
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        log("Using GITHUB_TOKEN from environment.")
        return token

    print()
    print("  A GitHub Personal Access Token (PAT) with 'repo' scope is required.")
    print("  Generate one at: https://github.com/settings/tokens")
    print("  Your input will not be displayed on screen.")
    print()
    token = getpass.getpass("  Enter your GitHub PAT: ").strip()

    if not token:
        log("No token provided. Aborting.", "ERR")
        sys.exit(1)

    return token


def run_git(args, cwd):
    """Run a git command and stream output, raising on failure."""
    result = subprocess.run(
        ["git"] + args,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        log(f"git {' '.join(args)} failed:", "ERR")
        print(result.stderr.strip())
        raise RuntimeError("Git command failed")
    return result.stdout.strip()


# ============================================================
# STEP 1 — CREATE ZIP ARCHIVE (for backup / release asset)
# ============================================================
def create_zip_archive():
    log("Creating zip archive of the site...")
    ZIP_OUTPUT_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_path = ZIP_OUTPUT_DIR / f"sytfix_{timestamp}.zip"

    file_count = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(SITE_DIR):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            root_path = Path(root)

            if any(part in EXCLUDE_DIRS for part in root_path.relative_to(SITE_DIR).parts):
                continue

            for file in files:
                if file in EXCLUDE_FILES:
                    continue
                file_path = root_path / file
                arcname = file_path.relative_to(SITE_DIR)
                zf.write(file_path, arcname)
                file_count += 1

    log(f"Archived {file_count} files → {zip_path.name}", "OK")
    return zip_path


# ============================================================
# STEP 2 — PUSH TO GITHUB
# ============================================================
def push_to_github(token):
    log(f"Preparing to push to github.com/{GITHUB_USERNAME}/{GITHUB_REPO} (branch: {BRANCH})...")

    git_dir = SITE_DIR / ".git"
    is_new_repo = not git_dir.exists()

    if is_new_repo:
        log("No existing .git directory found. Initializing new repository...")
        run_git(["init"], cwd=SITE_DIR)
        run_git(["branch", "-M", BRANCH], cwd=SITE_DIR)

    # Build authenticated remote URL (token is used only for this push, never saved to disk)
    remote_url = f"https://{GITHUB_USERNAME}:{token}@github.com/{GITHUB_USERNAME}/{GITHUB_REPO}.git"

    # Check if 'origin' remote already exists
    existing_remotes = run_git(["remote"], cwd=SITE_DIR)
    if "origin" in existing_remotes.split():
        run_git(["remote", "set-url", "origin", remote_url], cwd=SITE_DIR)
    else:
        run_git(["remote", "add", "origin", remote_url], cwd=SITE_DIR)

    log("Staging changes...")
    run_git(["add", "."], cwd=SITE_DIR)

    status = run_git(["status", "--porcelain"], cwd=SITE_DIR)
    if not status:
        log("No changes detected — nothing to commit.", "WARN")
        return False

    commit_msg = COMMIT_MESSAGE or f"Site update — {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    log(f"Committing: \"{commit_msg}\"")
    run_git(["commit", "-m", commit_msg], cwd=SITE_DIR)

    log("Pushing to GitHub (this triggers Vercel auto-deploy if connected)...")
    try:
        run_git(["push", "-u", "origin", BRANCH], cwd=SITE_DIR)
    except RuntimeError:
        log("Direct push failed — attempting pull-rebase then retry...", "WARN")
        run_git(["pull", "--rebase", "origin", BRANCH], cwd=SITE_DIR)
        run_git(["push", "-u", "origin", BRANCH], cwd=SITE_DIR)

    # IMPORTANT: scrub the token out of the stored remote URL after pushing,
    # so the PAT is never left sitting in .git/config on disk.
    safe_url = f"https://github.com/{GITHUB_USERNAME}/{GITHUB_REPO}.git"
    run_git(["remote", "set-url", "origin", safe_url], cwd=SITE_DIR)

    log("Push complete. Token scrubbed from local git config.", "OK")
    return True


# ============================================================
# STEP 3 — VERIFY REPO EXISTS (optional sanity check via API)
# ============================================================
def verify_repo_exists(token):
    log("Verifying repository exists on GitHub...")
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}

    try:
        resp = requests.get(url, headers=headers, timeout=10)
    except requests.RequestException as e:
        log(f"Could not reach GitHub API: {e}", "WARN")
        return True  # don't block deploy on a connectivity hiccup

    if resp.status_code == 200:
        log("Repository found.", "OK")
        return True
    elif resp.status_code == 404:
        log(f"Repository '{GITHUB_USERNAME}/{GITHUB_REPO}' not found.", "ERR")
        if confirm("Create it now as a private repository?"):
            create_resp = requests.post(
                "https://api.github.com/user/repos",
                headers=headers,
                json={"name": GITHUB_REPO, "private": True}
            )
            if create_resp.status_code == 201:
                log("Repository created.", "OK")
                return True
            else:
                log(f"Failed to create repository: {create_resp.text}", "ERR")
                return False
        return False
    else:
        log(f"Unexpected response checking repo ({resp.status_code}).", "WARN")
        return True


# ============================================================
# MAIN
# ============================================================
def main():
    print()
    print("  ╔══════════════════════════════════════╗")
    print("  ║        SytFix Deployment Script       ║")
    print("  ╚══════════════════════════════════════╝")
    print()

    if shutil.which("git") is None:
        log("Git is not installed or not on PATH. Install Git and try again.", "ERR")
        sys.exit(1)

    log(f"Site directory: {SITE_DIR}")

    if not confirm("Proceed with deployment?"):
        log("Cancelled by user.", "WARN")
        sys.exit(0)

    token = get_token()

    if not verify_repo_exists(token):
        log("Aborting deployment — repository not available.", "ERR")
        sys.exit(1)

    zip_path = create_zip_archive()

    pushed = push_to_github(token)

    print()
    if pushed:
        log("Deployment complete!", "OK")
        log(f"Backup archive saved at: {zip_path}")
        log(f"Check your Vercel dashboard for deployment status.")
    else:
        log("No changes were pushed (working tree was clean).", "WARN")
    print()


if __name__ == "__main__":
    main()
