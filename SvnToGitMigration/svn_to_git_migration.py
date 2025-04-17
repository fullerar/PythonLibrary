import argparse
from pathlib import Path
import re
import subprocess
import sys

from logger import Log  # <-- Import shared logger

def run_command(command, cwd=None):
    """
    Runs a shell command and returns stdout. Raises an error on failure.
    """
    Log.print("STEP", f"Running command: {command}")
    result = subprocess.run(command, cwd=cwd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        Log.print("ERROR", f"Command failed:\n{result.stderr.strip()}")
        sys.exit(1)
    return result.stdout.strip()

def extract_svn_authors(svn_url):
    """
    Uses `svn log` to gather all unique SVN usernames.
    """
    Log.print("STEP", "Extracting SVN authors...")
    log_output = run_command(f"svn log --quiet {svn_url}")
    authors = set()

    for line in log_output.splitlines():
        match = re.match(r"^r\d+ \| ([^|]+) \|", line)
        if match:
            authors.add(match.group(1).strip())

    author_map = {user: f"{user.title()} <{user}@example.com>" for user in sorted(authors)}
    Log.print("INFO", f"Found {len(author_map)} unique author(s).")
    return author_map

def write_authors_file(authors_dict, path):
    """
    Writes the authors.txt mapping file.
    """
    with open(path, 'w') as f:
        for username, identity in authors_dict.items():
            f.write(f"{username} = {identity}\n")
    Log.print("INFO", f"Authors file written to: {path}")

def migrate_svn_repo(svn_url, local_dir, authors_file):
    """
    Clones the SVN repository into a Git repo.
    """
    Log.print("STEP", "Cloning SVN repo using git-svn...")
    clone_command = (
        f"git svn clone {svn_url} "
        f"--stdlayout "
        f"--authors-file={authors_file} "
        f"--no-metadata "
        f"--prefix=svn/ "
        f"{local_dir}"
    )
    run_command(clone_command)
    Log.print("INFO", "SVN clone complete.")

def convert_svn_tags_to_git_tags(repo_dir):
    """
    Converts svn/tags/* branches into actual Git tags.
    """
    Log.print("STEP", "Converting SVN tag branches to Git tags...")
    remote_tags = run_command("git branch -r", cwd=repo_dir).splitlines()
    tag_refs = [line.strip() for line in remote_tags if line.strip().startswith("svn/tags/")]

    if not tag_refs:
        Log.print("WARN", "No SVN tags found to convert.")
        return

    for ref in tag_refs:
        tag_name = ref.split("svn/tags/")[-1]
        run_command(f"git tag {tag_name} {ref}", cwd=repo_dir)
        Log.print("INFO", f"Created Git tag: {tag_name}")

    for ref in tag_refs:
        run_command(f"git branch -rd {ref}", cwd=repo_dir)

def main():
    parser = argparse.ArgumentParser(description="Migrate an SVN repo to Git with history and tags.")
    parser.add_argument("--svn-url", required=True, help="URL of the SVN repository")
    parser.add_argument("--output-dir", default="svn_to_git_repo", help="Where to store the new Git repo")
    parser.add_argument("--log-file", help="Optional file to log output (disables terminal color)")

    args = parser.parse_args()

    if args.log_file:
        Log.set_log_file(args.log_file)

    output_path = Path(args.output_dir).resolve()
    authors_file = output_path.parent / "authors.txt"

    Log.print("STEP", "Starting SVN → Git migration...")

    # Step 1: Extract authors and write file
    svn_authors = extract_svn_authors(args.svn_url)
    write_authors_file(svn_authors, authors_file)

    # Step 2: Clone the repo
    migrate_svn_repo(args.svn_url, str(output_path), str(authors_file))

    # Step 3: Convert SVN-style tags
    convert_svn_tags_to_git_tags(str(output_path))

    Log.print("INFO", f"Migration complete. Git repo located at: {output_path}")

    Log.close()

if __name__ == "__main__":
    main()
