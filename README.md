# Github Manager

A Python tool for managing GitHub repositories and automating workflows following the global GitHub workflow instructions.

## Features

- **Repository Management**: Status checking, creation, cloning
- **Branch Operations**: Create, switch, merge, list branches
- **Commit Workflow**: Enhanced commit with smoke testing, revert, reset
- **Remote Operations**: Push, pull, remote management
- **Stash Management**: Stash and apply changes
- **History & Diff**: Commit history, file diffs, detailed status
- **Smoke Testing**: Comprehensive repository validation
- **GitHub CLI Integration**: Repository operations via GitHub CLI

## Requirements

- Python 3.6+
- Git
- GitHub CLI (for repository operations)

## Installation

1. Clone this repository
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

```bash
# Repository Status
python github_manager.py status
python github_manager.py branches

# Smoke Testing
python github_manager.py smoke-test

# Commit Operations
python github_manager.py commit "Your commit message"
python github_manager.py revert
python github_manager.py reset <commit-hash> [--hard]

# Branch Management
python github_manager.py branch <branch-name>
python github_manager.py checkout <branch-name>
python github_manager.py merge <source-branch> [target-branch]

# Remote Operations
python github_manager.py push [branch-name]
python github_manager.py pull [remote] [branch]
python github_manager.py remote-add <name> <url>

# Repository Operations
python github_manager.py create-repo repo-name [--private]
python github_manager.py clone repo-url [target-directory]

# Stash Operations
python github_manager.py stash [message]
python github_manager.py stash-pop [index]

# History & Diff
python github_manager.py history [limit]
python github_manager.py diff [file-path]
```

### Python API

```python
from github_manager import GithubManager

# Initialize manager
manager = GithubManager("/path/to/repo")

# Repository status
status = manager.get_repo_status()
print(f"Current branch: {status['current_branch']}")
print(f"Modified files: {status['modified_files']}")

# Branch operations
manager.create_branch("feature-branch")
manager.switch_branch("main")
manager.merge_branch("feature-branch")

# Commit workflow
if manager.smoke_test():
    manager.commit_changes("Update files")
    manager.push_to_github()

# Stash management
manager.stash_changes("Work in progress")
manager.stash_pop()

# History and diff
history = manager.get_commit_history(5)
diff = manager.get_file_diff("README.md")

# Advanced operations
manager.revert_last_commit()
manager.reset_to_commit("abc123", hard=False)
```

## Workflow Instructions

Following the global GitHub workflow rules:

1. **All code changes must be committed** - Use the `commit` method before pushing
2. **Smoke test requirement** - The `smoke_test()` method validates repository functionality
3. **Direct pushing** - No pull request required after smoke test passes
4. **Rollback plan** - Use `git revert` if issues are discovered

## Environment Setup

For new machines:
1. Install Python
2. Install VS Code
3. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```
