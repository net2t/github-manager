# Github Manager

A lightweight repo that contains:

- a **static web dashboard** (Netlify-ready) for browsing GitHub profile + repositories
- a **Python CLI** (`github_manager.py`) that helps you manage repos and follow a commit workflow with a required smoke test

## Live site

[git-hub-manager.netlify.app](https://git-hub-manager.netlify.app)

## Repository contents

- **Web dashboard (static)**
  - `github-manager-netlify.html` (main dashboard entry)
  - `index.html` (backup / alternate entry)
  - `netlify.toml` (Netlify publish + homepage redirect)
- **Python CLI**
  - `github_manager.py`
  - `requirements.txt` (no required external deps)

## Prerequisites

- **Git** installed and available on PATH
- **Python 3.8+** recommended (3.6+ may work)
- (Optional) **GitHub CLI** (`gh`) if you use features that rely on it

## Quick start

### 1) Clone

```bash
git clone https://github.com/net2t/github-manager.git
cd github-manager
```

### 2) Run the dashboard locally

This is a static HTML file.

- Open `github-manager-netlify.html` in your browser
- Enter a GitHub Personal Access Token (PAT) when prompted

If your browser blocks local fetch requests due to file URL restrictions, serve the folder with any static server (example with Python):

```bash
python -m http.server 8000
```

Then open:

`http://localhost:8000/github-manager-netlify.html`

### 3) Run the CLI smoke test

```bash
python github_manager.py smoke-test
```

## GitHub token (PAT) setup

The dashboard calls GitHub’s API from your browser.

1. Create a token on GitHub:
   - Settings
   - Developer settings
   - Personal access tokens
2. Recommended scopes:
   - `repo` (if you want private repos)
   - `read:user`
3. Paste the token into the dashboard UI

Security notes:

- **Do not commit tokens** to this repository.
- The dashboard may store the token in `localStorage` for convenience; use a separate browser profile if you want isolation.

## Python CLI usage

### Install (optional)

This project is designed to run without external dependencies.

```bash
pip install -r requirements.txt
```

### Common commands

```bash
# Repository status / branches
python github_manager.py status
python github_manager.py branches

# Smoke testing (run before pushing changes)
python github_manager.py smoke-test

# Commit workflow
python github_manager.py commit "Your commit message"
python github_manager.py revert
python github_manager.py reset <commit-hash> [--hard]

# Branch management
python github_manager.py branch <branch-name>
python github_manager.py checkout <branch-name>
python github_manager.py merge <source-branch> [target-branch]

# Remote operations
python github_manager.py push [branch-name]
python github_manager.py pull [remote] [branch]
python github_manager.py remote-add <name> <url>

# Repo operations
python github_manager.py create-repo repo-name [--private]
python github_manager.py clone repo-url [target-directory]

# Stash
python github_manager.py stash [message]
python github_manager.py stash-pop [index]

# History & diff
python github_manager.py history [limit]
python github_manager.py diff [file-path]
```

## Deployment (Netlify)

This repo is configured for static deploy.

- **Publish directory**: `.` (repo root)
- **Homepage**: `/` redirects to `/github-manager-netlify.html`

### Deploy from Git (recommended)

1. Create a new site in Netlify
2. Connect the GitHub repo
3. Build settings:
   - Build command: *(none)*
   - Publish directory: `.`

### Deploy by drag & drop

You can also deploy by dragging the `github-manager-netlify.html` file (or the whole folder) into Netlify’s manual deploy.

## Troubleshooting

### Dashboard shows API errors

- Confirm your PAT is valid
- Confirm scopes (`read:user`, and `repo` if needed)
- GitHub API is rate-limited; authenticated requests have higher limits

### Local file doesn’t load data

Some browsers restrict network requests from `file://` pages.

- Use `python -m http.server` and open `http://localhost:8000/...`

### CLI commands fail

- Ensure `git` is installed
- Run `python github_manager.py smoke-test` to validate the environment
