import os
import subprocess
from typing import List

class GitService:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        if not os.path.exists(repo_path):
            os.makedirs(repo_path)
            subprocess.run(["git", "-C", repo_path, "init"])

    def list_files(self) -> List[str]:
        """Retourne la liste des fichiers suivis par Git"""
        result = subprocess.run(
            ["git", "-C", self.repo_path, "ls-files"],
            capture_output=True, text=True
        )
        return result.stdout.splitlines()

    def add_file(self, filename: str, commit_message: str):
        """Ajoute un fichier et fait un commit"""
        subprocess.run(["git", "-C", self.repo_path, "add", filename])
        subprocess.run(["git", "-C", self.repo_path, "commit", "-m", commit_message])

    def get_history(self, filename: str) -> str:
        """Retourne l’historique des commits pour un fichier"""
        result = subprocess.run(
            ["git", "-C", self.repo_path, "log", "--", filename],
            capture_output=True, text=True
        )
        return result.stdout
