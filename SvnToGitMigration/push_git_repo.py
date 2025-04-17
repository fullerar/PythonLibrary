import argparse
import subprocess
from pathlib import Path
import sys

from logger import Log

def run_command(command, cwd=None):
    Log.print("STEP", f"Running command: {command}")
    result = subprocess.run(command, cwd=cwd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        Log.print("ERROR", f"Command failed:\n{result.stderr.strip()}")
        sys.exit(1)
    return result.stdout.strip()

def push_to_remote_git(repo_dir, remote_url):
    run_command(f"git remote add origin {remote_url}", cwd=repo_dir)
    run_command("git push origin --all", cwd=repo_dir)
    run_command("git push origin --tags", cwd=repo_dir)
    Log.print("INFO", "All branches and tags pushed to remote.")

def main():
    parser = argparse.ArgumentParser(description="Push a local Git repo (converted from SVN) to a remote Git server.")
    parser.add_argument("--repo-dir", required=True, help="Path to the Git repo")
    parser.add_argument("--remote-url", required=True, help="Destination Git remote URL")
    parser.add_argument("--log-file", help="Optional file to log output")

    args = parser.parse_args()

    if args.log_file:
        Log.set_log_file(args.log_file)

    repo_path = Path(args.repo_dir).resolve()
    if not (repo_path / ".git").exists():
        Log.print("ERROR", f"'{repo_path}' is not a Git repo (missing .git)")
        sys.exit(1)

    Log.print("STEP", f"Pushing Git repo at {repo_path} to {args.remote_url}")
    push_to_remote_git(str(repo_path), args.remote_url)
    Log.close()

if __name__ == "__main__":
    main()
