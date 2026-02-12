#!/usr/bin/env python3
"""
Github Manager - A tool for managing GitHub repositories and automating workflows
"""

import os
import subprocess
import json
import datetime
import re
from typing import Dict, List, Optional, Tuple
from pathlib import Path

class GithubManager:
    def __init__(self, repo_path: str = None):
        self.repo_path = repo_path or os.getcwd()
        self.git_dir = os.path.join(self.repo_path, '.git')
        
    def is_git_repo(self) -> bool:
        """Check if current directory is a git repository"""
        return os.path.exists(self.git_dir)
    
    def get_repo_status(self) -> Dict:
        """Get current repository status with detailed information"""
        if not self.is_git_repo():
            return {"error": "Not a git repository"}
        
        try:
            # Get git status
            result = subprocess.run(
                ['git', 'status', '--porcelain', '-b'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            # Get current branch
            branch_result = subprocess.run(
                ['git', 'branch', '--show-current'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            # Get remote info
            remote_result = subprocess.run(
                ['git', 'remote', '-v'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            # Get last commit info
            commit_result = subprocess.run(
                ['git', 'log', '-1', '--format=%H|%s|%ai|%an'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            # Parse status output
            status_lines = result.stdout.strip().split('\n')
            branch_line = status_lines[0] if status_lines else ""
            
            # Count changes by type
            modified = []
            added = []
            deleted = []
            untracked = []
            
            for line in status_lines[1:]:
                if line.strip():
                    status_code = line[:2]
                    file_path = line[3:]
                    
                    if status_code.startswith(' M') or status_code.startswith('M'):
                        modified.append(file_path)
                    elif status_code.startswith('A'):
                        added.append(file_path)
                    elif status_code.startswith('D'):
                        deleted.append(file_path)
                    elif status_code.startswith('??'):
                        untracked.append(file_path)
            
            # Parse commit info
            commit_info = {}
            if commit_result.stdout.strip():
                commit_hash, message, date, author = commit_result.stdout.strip().split('|')
                commit_info = {
                    "hash": commit_hash,
                    "message": message,
                    "date": date,
                    "author": author
                }
            
            return {
                "current_branch": branch_result.stdout.strip(),
                "status": result.stdout.strip(),
                "has_changes": bool(result.stdout.strip()),
                "modified_files": modified,
                "added_files": added,
                "deleted_files": deleted,
                "untracked_files": untracked,
                "remotes": remote_result.stdout.strip().split('\n') if remote_result.stdout.strip() else [],
                "last_commit": commit_info,
                "is_ahead": 'ahead' in branch_line,
                "is_behind": 'behind' in branch_line
            }
        except Exception as e:
            return {"error": str(e)}
    
    def smoke_test(self) -> bool:
        """Run comprehensive smoke test to ensure repository is functional"""
        if not self.is_git_repo():
            print("Error: Not a git repository")
            return False
        
        try:
            # Test basic git operations
            print("Running smoke tests...")
            
            # Test git status
            subprocess.run(['git', 'status'], cwd=self.repo_path, check=True, capture_output=True)
            print("✓ Git status command works")
            
            # Test git log
            subprocess.run(['git', 'log', '--oneline', '-1'], cwd=self.repo_path, check=True, capture_output=True)
            print("✓ Git log command works")
            
            # Test remote connection (if remotes exist)
            status = self.get_repo_status()
            if status.get('remotes'):
                try:
                    subprocess.run(['git', 'remote', 'show', 'origin'], cwd=self.repo_path, check=True, capture_output=True, timeout=10)
                    print("✓ Remote connection works")
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                    print("⚠ Remote connection failed (offline or no access)")
            
            print("✓ All smoke tests passed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Smoke test failed: {e}")
            return False
    
    def commit_changes(self, message: str, add_all: bool = True) -> bool:
        """Commit current changes with options"""
        if not self.smoke_test():
            return False
        
        try:
            # Check if there are changes to commit
            status = self.get_repo_status()
            if not status.get('has_changes') and not status.get('untracked_files'):
                print("No changes to commit")
                return True
            
            if add_all:
                # Add all changes
                subprocess.run(['git', 'add', '.'], cwd=self.repo_path, check=True)
                print("✓ All changes staged")
            
            # Commit changes
            subprocess.run(['git', 'commit', '-m', message], cwd=self.repo_path, check=True)
            print(f"✓ Changes committed: {message}")
            return True
        except subprocess.CalledProcessError as e:
            if "nothing to commit" in str(e):
                print("No changes to commit")
                return True
            print(f"✗ Commit failed: {e}")
            return False
    
    def push_to_github(self, branch: str = None) -> bool:
        """Push changes to GitHub"""
        if not self.smoke_test():
            return False
        
        try:
            if branch:
                subprocess.run(['git', 'push', 'origin', branch], cwd=self.repo_path, check=True)
            else:
                subprocess.run(['git', 'push'], cwd=self.repo_path, check=True)
            print("✓ Changes pushed to GitHub")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Push failed: {e}")
            return False
    
    def create_repository(self, repo_name: str, private: bool = False) -> bool:
        """Create a new GitHub repository using GitHub CLI"""
        try:
            cmd = ['gh', 'repo', 'create', repo_name]
            if private:
                cmd.append('--private')
            else:
                cmd.append('--public')
            
            subprocess.run(cmd, cwd=self.repo_path, check=True)
            print(f"✓ Repository '{repo_name}' created on GitHub")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Repository creation failed: {e}")
            return False
    
    def clone_repository(self, repo_url: str, target_dir: str = None) -> bool:
        """Clone a GitHub repository"""
        try:
            if target_dir:
                subprocess.run(['git', 'clone', repo_url, target_dir], check=True)
                print(f"✓ Repository cloned to '{target_dir}'")
            else:
                subprocess.run(['git', 'clone', repo_url], check=True)
                print("✓ Repository cloned")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Clone failed: {e}")
            return False
    
    def create_branch(self, branch_name: str, checkout: bool = True) -> bool:
        """Create and optionally checkout a new branch"""
        if not self.is_git_repo():
            print("Error: Not a git repository")
            return False
        
        try:
            if checkout:
                subprocess.run(['git', 'checkout', '-b', branch_name], cwd=self.repo_path, check=True)
                print(f"✓ Created and checked out branch '{branch_name}'")
            else:
                subprocess.run(['git', 'branch', branch_name], cwd=self.repo_path, check=True)
                print(f"✓ Created branch '{branch_name}'")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Branch creation failed: {e}")
            return False
    
    def switch_branch(self, branch_name: str) -> bool:
        """Switch to an existing branch"""
        if not self.is_git_repo():
            print("Error: Not a git repository")
            return False
        
        try:
            subprocess.run(['git', 'checkout', branch_name], cwd=self.repo_path, check=True)
            print(f"✓ Switched to branch '{branch_name}'")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Branch switch failed: {e}")
            return False
    
    def merge_branch(self, source_branch: str, target_branch: str = None) -> bool:
        """Merge a branch into current or target branch"""
        if not self.is_git_repo():
            print("Error: Not a git repository")
            return False
        
        try:
            current_branch = self.get_repo_status().get('current_branch')
            
            if target_branch and target_branch != current_branch:
                # Switch to target branch first
                subprocess.run(['git', 'checkout', target_branch], cwd=self.repo_path, check=True)
                print(f"✓ Switched to branch '{target_branch}'")
            
            # Merge source branch
            subprocess.run(['git', 'merge', source_branch], cwd=self.repo_path, check=True)
            print(f"✓ Merged branch '{source_branch}' into '{target_branch or current_branch}'")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Merge failed: {e}")
            return False
    
    def pull_changes(self, remote: str = 'origin', branch: str = None) -> bool:
        """Pull changes from remote repository"""
        if not self.is_git_repo():
            print("Error: Not a git repository")
            return False
        
        try:
            if branch:
                subprocess.run(['git', 'pull', remote, branch], cwd=self.repo_path, check=True)
                print(f"✓ Pulled changes from {remote}/{branch}")
            else:
                subprocess.run(['git', 'pull'], cwd=self.repo_path, check=True)
                print(f"✓ Pulled changes from {remote}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Pull failed: {e}")
            return False
    
    def get_commit_history(self, limit: int = 10) -> List[Dict]:
        """Get commit history with details"""
        if not self.is_git_repo():
            return [{"error": "Not a git repository"}]
        
        try:
            result = subprocess.run(
                ['git', 'log', f'--oneline=-{limit}', '--format=%H|%s|%ai|%an'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            commits = []
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    commit_hash, message, date, author = line.split('|')
                    commits.append({
                        "hash": commit_hash,
                        "message": message,
                        "date": date,
                        "author": author
                    })
            
            return commits
        except Exception as e:
            return [{"error": str(e)}]
    
    def stash_changes(self, message: str = None) -> bool:
        """Stash current changes"""
        if not self.is_git_repo():
            print("Error: Not a git repository")
            return False
        
        try:
            if message:
                subprocess.run(['git', 'stash', 'push', '-m', message], cwd=self.repo_path, check=True)
                print(f"✓ Changes stashed with message: {message}")
            else:
                subprocess.run(['git', 'stash'], cwd=self.repo_path, check=True)
                print("✓ Changes stashed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Stash failed: {e}")
            return False
    
    def stash_pop(self, stash_index: str = '0') -> bool:
        """Pop stashed changes"""
        if not self.is_git_repo():
            print("Error: Not a git repository")
            return False
        
        try:
            subprocess.run(['git', 'stash', 'pop', f'stash@{{{stash_index}}}'], cwd=self.repo_path, check=True)
            print(f"✓ Stashed changes applied (stash@{{{stash_index}}})")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Stash pop failed: {e}")
            return False
    
    def get_file_diff(self, file_path: str = None, staged: bool = False) -> str:
        """Get diff for specific file or all changes"""
        if not self.is_git_repo():
            return "Error: Not a git repository"
        
        try:
            cmd = ['git', 'diff']
            if staged:
                cmd.append('--staged')
            if file_path:
                cmd.append(file_path)
            
            result = subprocess.run(cmd, cwd=self.repo_path, capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return f"Error getting diff: {e}"
    
    def revert_last_commit(self) -> bool:
        """Revert the last commit"""
        if not self.is_git_repo():
            print("Error: Not a git repository")
            return False
        
        try:
            subprocess.run(['git', 'revert', 'HEAD'], cwd=self.repo_path, check=True)
            print("✓ Last commit reverted")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Revert failed: {e}")
            return False
    
    def reset_to_commit(self, commit_hash: str, hard: bool = False) -> bool:
        """Reset repository to specific commit"""
        if not self.is_git_repo():
            print("Error: Not a git repository")
            return False
        
        try:
            cmd = ['git', 'reset']
            if hard:
                cmd.append('--hard')
            cmd.append(commit_hash)
            
            mode = "hard" if hard else "soft"
            subprocess.run(cmd, cwd=self.repo_path, check=True)
            print(f"✓ Reset to commit {commit_hash} ({mode} mode)")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Reset failed: {e}")
            return False
    
    def add_remote(self, name: str, url: str) -> bool:
        """Add a new remote repository"""
        if not self.is_git_repo():
            print("Error: Not a git repository")
            return False
        
        try:
            subprocess.run(['git', 'remote', 'add', name, url], cwd=self.repo_path, check=True)
            print(f"✓ Added remote '{name}': {url}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Adding remote failed: {e}")
            return False
    
    def list_branches(self, remote: bool = False) -> List[str]:
        """List all branches"""
        if not self.is_git_repo():
            return ["Error: Not a git repository"]
        
        try:
            cmd = ['git', 'branch']
            if remote:
                cmd.append('-r')
            cmd.append('-a')
            
            result = subprocess.run(cmd, cwd=self.repo_path, capture_output=True, text=True)
            branches = [b.strip().replace('* ', '') for b in result.stdout.strip().split('\n') if b.strip()]
            return branches
        except Exception as e:
            return [f"Error: {e}"]

def main():
    """Main function for command-line usage"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python github_manager.py <command> [options]")
        print("Commands:")
        print("  status                    - Show repository status")
        print("  smoke-test               - Run smoke tests")
        print("  commit <message>         - Commit changes")
        print("  push [branch]            - Push to GitHub")
        print("  pull [remote] [branch]   - Pull from remote")
        print("  create-repo <name>       - Create new repository")
        print("  clone <url> [dir]        - Clone repository")
        print("  branch <name>            - Create and checkout branch")
        print("  checkout <name>          - Switch to branch")
        print("  merge <source> [target]  - Merge branches")
        print("  history [limit]          - Show commit history")
        print("  stash [message]          - Stash changes")
        print("  stash-pop [index]        - Apply stashed changes")
        print("  diff [file]              - Show diff")
        print("  revert                   - Revert last commit")
        print("  reset <hash> [--hard]    - Reset to commit")
        print("  branches                 - List all branches")
        print("  remote-add <name> <url>  - Add remote repository")
        return
    
    manager = GithubManager()
    command = sys.argv[1].lower()
    
    if command == "status":
        status = manager.get_repo_status()
        print(json.dumps(status, indent=2))
    
    elif command == "smoke-test":
        manager.smoke_test()
    
    elif command == "commit" and len(sys.argv) > 2:
        message = " ".join(sys.argv[2:])
        manager.commit_changes(message)
    
    elif command == "push":
        branch = sys.argv[2] if len(sys.argv) > 2 else None
        manager.push_to_github(branch)
    
    elif command == "pull":
        remote = sys.argv[2] if len(sys.argv) > 2 else 'origin'
        branch = sys.argv[3] if len(sys.argv) > 3 else None
        manager.pull_changes(remote, branch)
    
    elif command == "create-repo" and len(sys.argv) > 2:
        repo_name = sys.argv[2]
        private = "--private" in sys.argv
        manager.create_repository(repo_name, private)
    
    elif command == "clone" and len(sys.argv) > 2:
        repo_url = sys.argv[2]
        target_dir = sys.argv[3] if len(sys.argv) > 3 else None
        manager.clone_repository(repo_url, target_dir)
    
    elif command == "branch" and len(sys.argv) > 2:
        branch_name = sys.argv[2]
        manager.create_branch(branch_name)
    
    elif command == "checkout" and len(sys.argv) > 2:
        branch_name = sys.argv[2]
        manager.switch_branch(branch_name)
    
    elif command == "merge" and len(sys.argv) > 2:
        source_branch = sys.argv[2]
        target_branch = sys.argv[3] if len(sys.argv) > 3 else None
        manager.merge_branch(source_branch, target_branch)
    
    elif command == "history":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        history = manager.get_commit_history(limit)
        for commit in history:
            if 'error' in commit:
                print(f"Error: {commit['error']}")
            else:
                print(f"{commit['hash'][:8]} - {commit['author']} - {commit['date'][:10]} - {commit['message']}")
    
    elif command == "stash":
        message = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else None
        manager.stash_changes(message)
    
    elif command == "stash-pop":
        stash_index = sys.argv[2] if len(sys.argv) > 2 else '0'
        manager.stash_pop(stash_index)
    
    elif command == "diff":
        file_path = sys.argv[2] if len(sys.argv) > 2 else None
        diff = manager.get_file_diff(file_path)
        print(diff)
    
    elif command == "revert":
        manager.revert_last_commit()
    
    elif command == "reset" and len(sys.argv) > 2:
        commit_hash = sys.argv[2]
        hard = "--hard" in sys.argv
        manager.reset_to_commit(commit_hash, hard)
    
    elif command == "branches":
        branches = manager.list_branches()
        for branch in branches:
            print(f"  {branch}")
    
    elif command == "remote-add" and len(sys.argv) > 3:
        name = sys.argv[2]
        url = sys.argv[3]
        manager.add_remote(name, url)
    
    else:
        print("Invalid command or missing arguments")
        print("Use 'python github_manager.py' to see available commands")

if __name__ == "__main__":
    main()
