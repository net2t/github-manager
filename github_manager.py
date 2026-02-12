#!/usr/bin/env python3
"""
Github Manager - A tool for managing GitHub repositories and automating workflows
"""

import os
import subprocess
import json
from typing import Dict, List, Optional
from pathlib import Path

class GithubManager:
    def __init__(self, repo_path: str = None):
        self.repo_path = repo_path or os.getcwd()
        self.git_dir = os.path.join(self.repo_path, '.git')
        
    def is_git_repo(self) -> bool:
        """Check if current directory is a git repository"""
        return os.path.exists(self.git_dir)
    
    def get_repo_status(self) -> Dict:
        """Get current repository status"""
        if not self.is_git_repo():
            return {"error": "Not a git repository"}
        
        try:
            # Get git status
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
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
            
            return {
                "current_branch": branch_result.stdout.strip(),
                "status": result.stdout.strip(),
                "has_changes": bool(result.stdout.strip())
            }
        except Exception as e:
            return {"error": str(e)}
    
    def smoke_test(self) -> bool:
        """Run smoke test to ensure repository is functional"""
        if not self.is_git_repo():
            print("Error: Not a git repository")
            return False
        
        try:
            # Test basic git operations
            subprocess.run(['git', 'status'], cwd=self.repo_path, check=True, capture_output=True)
            print("✓ Git repository is functional")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Smoke test failed: {e}")
            return False
    
    def commit_changes(self, message: str) -> bool:
        """Commit current changes"""
        if not self.smoke_test():
            return False
        
        try:
            # Add all changes
            subprocess.run(['git', 'add', '.'], cwd=self.repo_path, check=True)
            
            # Commit changes
            subprocess.run(['git', 'commit', '-m', message], cwd=self.repo_path, check=True)
            print(f"✓ Changes committed: {message}")
            return True
        except subprocess.CalledProcessError as e:
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

def main():
    """Main function for command-line usage"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python github_manager.py <command> [options]")
        print("Commands: status, smoke-test, commit, push, create-repo, clone")
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
    
    elif command == "create-repo" and len(sys.argv) > 2:
        repo_name = sys.argv[2]
        private = "--private" in sys.argv
        manager.create_repository(repo_name, private)
    
    elif command == "clone" and len(sys.argv) > 2:
        repo_url = sys.argv[2]
        target_dir = sys.argv[3] if len(sys.argv) > 3 else None
        manager.clone_repository(repo_url, target_dir)
    
    else:
        print("Invalid command or missing arguments")

if __name__ == "__main__":
    main()
