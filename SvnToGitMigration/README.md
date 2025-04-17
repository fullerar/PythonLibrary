# SVN to Git Migration Toolkit

This toolkit contains 3 modular Python scripts to help you **safely migrate an SVN repository to Git**, preserving full history, authorship, branches, and tags.

It includes:
- ✅ Terminal color output for clarity
- 📝 Optional logging to file with structured `[INFO]`, `[WARN]`, `[STEP]` tags

---

## 📦 Requirements

- Python 3.6+
- `git`, `git-svn`, and `svn` command-line tools installed

On Ubuntu:
```bash
sudo apt install git git-svn subversion
```

---

## 📂 Folder Structure

```
migration_tools/
├── logger.py                 # Shared logging utility
├── svn_to_git_migration.py  # Step 1: Clone + convert
├── validate_git_repo.py     # Step 2: Inspect + compare with SVN
├── push_git_repo.py         # Step 3: Push final result to Git host
└── README.md                # This file
```

---

## 🚀 Usage Workflow

### 1️⃣ Migrate SVN repo to Git
```bash
python3 svn_to_git_migration.py \
  --svn-url https://svn.example.com/myproject \
  --output-dir ./myproject_git \
  --log-file migration_log.txt  # Optional
```

### 2️⃣ Validate migration
```bash
python3 validate_git_repo.py \
  --repo-dir ./myproject_git \
  --svn-url https://svn.example.com/myproject \
  --log-file validate_log.txt  # Optional
```

### 3️⃣ Push to Git remote (GitHub, GitLab, etc.)
```bash
python3 push_git_repo.py \
  --repo-dir ./myproject_git \
  --remote-url https://github.com/youruser/myproject.git \
  --log-file push_log.txt  # Optional
```

---

## 🖥 Output Options

| Mode          | Description                         |
|---------------|-------------------------------------|
| Terminal only | Full color with tags like `[INFO]`  |
| Log file only | Plain text with `[INFO]`, `[WARN]`  |

Use `--log-file your_log.txt` to save structured output to a file. When this flag is used, terminal color is automatically disabled.

---

## 🧠 How It Works

- `svn_to_git_migration.py`:  
  - Pulls SVN commit history
  - Extracts unique authors
  - Converts tags properly

- `validate_git_repo.py`:  
  - Checks that all commits, branches, and tags are in place
  - Compares Git output with actual SVN structure

- `push_git_repo.py`:  
  - Pushes all Git refs to a specified remote

---

## ✅ Status Indicators

| Tag    | Meaning                            |
|--------|------------------------------------|
| `[STEP]`  | High-level process stage          |
| `[INFO]`  | Informational messages            |
| `[WARN]`  | Something might be missing/wrong  |
| `[ERROR]` | Critical failure (script stops)   |

---

## 🛠️ Tips

- You can run these scripts independently or wrap them in a shell script for automation.
- Customize the author name/email mapping in `authors.txt` if desired (auto-generated).
- Review converted tags carefully — some SVN tags may not convert perfectly if their structure was non-standard.

---

## 📃 License

MIT License