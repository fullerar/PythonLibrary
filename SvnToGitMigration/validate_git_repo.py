import argparse
import subprocess
from pathlib import Path
import re
import sys

from logger import Log  # <-- shared logger module

def run_command(command, cwd=None):
    Log.print("STEP", f"Running command: {command}")
    result = subprocess.run(command, cwd=cwd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        Log.print("ERROR", f"Command failed:\n{result.stderr.strip()}")
        sys.exit(1)
    return result.stdout.strip()

def list_svn_dirs(svn_url, subpath):
    try:
        result = run_command(f"svn ls {svn_url.rstrip('/')}/{subpath.strip('/')}/")
        entries = [line.strip('/').strip() for line in result.splitlines() if line]
        return set(entries)
    except Exception as e:
        Log.print("WARN", f"Could not list SVN path '{subpath}': {e}")
        return set()

def validate_git_repo(path, svn_url=None):
    path = Path(path).resolve()
    Log.print("STEP", f"Validating Git repo at: {path}")

    if not path.exists():
        Log.print("ERROR", f"Path does not exist: {path}")
        sys.exit(1)

    try:
        run_command("git rev-parse --is-inside-work-tree", cwd=path)
        Log.print("INFO", "Valid Git repository confirmed.")
    except:
        Log.print("ERROR", "Not a valid Git repository (missing .git)")
        sys.exit(1)

    svn_dir = path / ".git" / "svn"
    if svn_dir.exists():
        Log.print("INFO", "Detected Git-SVN migration (.git/svn present)")
    else:
        Log.print("WARN", "No .git/svn found — may not be a Git-SVN clone")

    # Git summary
    Log.print("STEP", "Fetching Git summary...")
    Log.print("INFO", "Recent commits:")
    print(run_command("git log --oneline -n 5", cwd=path))

    git_branches = set(run_command("git branch -a", cwd=path).replace("* ", "").replace("remotes/", "").split())
    git_tags = set(run_command("git tag", cwd=path).splitlines())

    Log.print("INFO", f"Found {len(git_branches)} branches and {len(git_tags)} tags in Git.")

    # Compare with SVN if URL provided
    if svn_url:
        Log.print("STEP", "Comparing against SVN layout...")
        svn_branches = list_svn_dirs(svn_url, "branches")
        svn_tags = list_svn_dirs(svn_url, "tags")

        missing_branches = svn_branches - git_branches
        missing_tags = svn_tags - git_tags

        if missing_branches:
            Log.print("WARN", "Missing branches:")
            for b in sorted(missing_branches):
                Log.print("WARN", f"  → {b}")
        else:
            Log.print("INFO", "All SVN branches accounted for.")

        if missing_tags:
            Log.print("WARN", "Missing tags:")
            for t in sorted(missing_tags):
                Log.print("WARN", f"  → {t}")
        else:
            Log.print("INFO", "All SVN tags accounted for.")

    Log.print("STEP", "Validation complete.")
    Log.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate a Git repo converted from SVN.")
    parser.add_argument("--repo-dir", required=True, help="Path to the Git repo")
    parser.add_argument("--svn-url", help="Original SVN URL to compare branches/tags")
    parser.add_argument("--log-file", help="Optional file to write log output")

    args = parser.parse_args()

    if args.log_file:
        Log.set_log_file(args.log_file)

    validate_git_repo(args.repo_dir, args.svn_url)
