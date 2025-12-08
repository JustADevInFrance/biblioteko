import os
import shutil
import subprocess
from typing import List

class GitService:
    """
    Service Git central pour gérer :
    - création de comptes utilisateurs avec configuration Git
    - branches utilisateur
    - dépôt modération
    - validation / rejet
    """
    REQUIRED_DIRS = ["fond_commun", "a_moderer", "sequestre", "users"]

    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        os.makedirs(repo_path, exist_ok=True)

        # Init repo Git si nécessaire
        if not os.path.exists(os.path.join(repo_path, ".git")):
            subprocess.run(["git", "-C", self.repo_path, "init", "-b", "main"], check=True)


        # Assure la présence des répertoires
        self._ensure_base_directories()

        # Branches principales
        self._ensure_branch("main")
        self._ensure_branch("moderation")

    # ────────────── Gestion des répertoires ──────────────
    def _ensure_base_directories(self):
        for d in self.REQUIRED_DIRS:
            os.makedirs(os.path.join(self.repo_path, d), exist_ok=True)
        subprocess.run(["git", "-C", self.repo_path, "add", "."], check=True)
        subprocess.run(["git", "-C", self.repo_path, "commit", "-m", "Initialisation des répertoires"], check=False)

    # ────────────── Gestion des branches ──────────────
    def _ensure_branch(self, branch: str):
        result = subprocess.run(
            ["git", "-C", self.repo_path, "branch", "--list", branch],
            capture_output=True, text=True
        )
        if result.stdout.strip() == "":
            subprocess.run(["git", "-C", self.repo_path, "checkout", "-b", branch], check=True)
            subprocess.run(["git", "-C", self.repo_path, "checkout", "main"], check=True)

    # ────────────── Création utilisateur ──────────────
    def create_user(self, prenom: str, nom: str, email: str):
        username = f"{prenom.lower()}_{nom.lower()}"
        branch_name = f"user/{username}"

        # Configure Git localement
        subprocess.run(["git", "-C", self.repo_path, "config", "user.name", f"{prenom} {nom}"], check=True)
        subprocess.run(["git", "-C", self.repo_path, "config", "user.email", email], check=True)

        # Création branche utilisateur
        self._ensure_branch(branch_name)

        # Création dossier utilisateur
        user_folder = os.path.join(self.repo_path, "users", username)
        os.makedirs(user_folder, exist_ok=True)

        subprocess.run(["git", "-C", self.repo_path, "add", "."], check=True)
        subprocess.run(["git", "-C", self.repo_path, "commit", "-m", f"Création compte utilisateur {username}"], check=False)

        return username

    # ────────────── Upload utilisateur ──────────────
    def upload_user_file(self, username: str, filename: str, content: bytes):
        branch = f"user/{username}"
        self._ensure_branch(branch)

        # Checkout branche utilisateur
        subprocess.run(["git", "-C", self.repo_path, "checkout", branch], check=True)

        path = os.path.join(self.repo_path, "users", username, filename)
        with open(path, "wb") as f:
            f.write(content)

        subprocess.run(["git", "-C", self.repo_path, "add", path], check=True)
        subprocess.run(["git", "-C", self.repo_path, "commit", "-m", f"Upload fichier {filename}"], check=True)

        # Copier dans la branche moderation
        self.send_to_moderation(username, filename)

        return path

    # ────────────── Déplacement vers modération ──────────────
    def send_to_moderation(self, username: str, filename: str):
        subprocess.run(["git", "-C", self.repo_path, "checkout", "moderation"], check=True)
        src = os.path.join(self.repo_path, "users", username, filename)
        dest = os.path.join(self.repo_path, "a_moderer", f"{username}__{filename}")
        shutil.copy(src, dest)
        subprocess.run(["git", "-C", self.repo_path, "add", dest], check=True)
        subprocess.run(["git", "-C", self.repo_path, "commit", "-m", f"{filename} en attente de modération"], check=True)

    # ────────────── Modération ──────────────
    def list_moderation_files(self) -> List[str]:
        return os.listdir(os.path.join(self.repo_path, "a_moderer"))

    def approve(self, mod_filename: str, libre=True):
        src = os.path.join(self.repo_path, "a_moderer", mod_filename)
        dest_folder = "fond_commun" if libre else "sequestre"
        dest = os.path.join(self.repo_path, dest_folder, mod_filename)
        shutil.move(src, dest)
        subprocess.run(["git", "-C", self.repo_path, "add", "."], check=True)
        subprocess.run(["git", "-C", self.repo_path, "commit", "-m", f"Validation : {mod_filename}"], check=True)
        return dest

    def reject(self, mod_filename: str, commentaire: str = ""):
        src = os.path.join(self.repo_path, "a_moderer", mod_filename)
        os.remove(src)
        subprocess.run(["git", "-C", self.repo_path, "add", "."], check=True)
        subprocess.run(["git", "-C", self.repo_path, "commit", "-m", f"Rejet : {mod_filename} | {commentaire}"], check=True)
