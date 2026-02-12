# Github Manager

A Python tool for managing GitHub repositories and automating workflows following the global GitHub workflow instructions.

## Features

- Repository status checking
- Smoke testing before operations
- Automated commit and push workflows
- Repository creation and cloning
- Integration with GitHub CLI

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
# Check repository status
python github_manager.py status

# Run smoke test
python github_manager.py smoke-test

# Commit changes
python github_manager.py commit "Your commit message"

# Push to GitHub
python github_manager.py push [branch-name]

# Create new repository
python github_manager.py create-repo repo-name [--private]

# Clone repository
python github_manager.py clone repo-url [target-directory]
```

### Python API

```python
from github_manager import GithubManager

# Initialize manager
manager = GithubManager("/path/to/repo")

# Run smoke test
if manager.smoke_test():
    # Commit and push changes
    manager.commit_changes("Update files")
    manager.push_to_github()
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
