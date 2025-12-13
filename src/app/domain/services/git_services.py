import os
import shutil
import subprocess
from typing import List


class GitService:
    """
    Service Git spécialisé pour Biblioteko.
    Gère :
    - dépôt Git
    - branches (master, moderation)
    - répertoires : fond_commun, a_moderer, sequestre
    - modération (approve/reject)
    """

    DEFAULT_DIRECTORIES = ["fond_commun", "a_moderer", "sequestre"]
    DEFAULT_BRANCHES = ["moderation"]

    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        os.makedirs(repo_path, exist_ok=True)

        # Init du repo si nécessaire
        if not os.path.exists(os.path.join(repo_path, ".git")):
            subprocess.run(["git", "-C", repo_path, "init"], check=True)
            subprocess.run(
                ["git", "-C", repo_path, "config", "user.name", "jonas numa"], check=True
            )
            subprocess.run(
                ["git", "-C", repo_path, "config", "user.email", "jonas.numa.etu@univ-lille.fr"], check=True
            )

            # Commit initial pour pouvoir créer des branches
            for d in self.DEFAULT_DIRECTORIES:
                os.makedirs(os.path.join(repo_path, d), exist_ok=True)
            subprocess.run(["git", "-C", repo_path, "commit", "--allow-empty", "-m", "Initial commit"], check=True)

        # Création des branches si elles n'existent pas
        self._ensure_branches()

        # Création des répertoires requis
        self._ensure_directories()


    def _ensure_directories(self):
        """Créer les répertoires par défaut s'ils n'existent pas"""
        for d in self.DEFAULT_DIRECTORIES:
            path = os.path.join(self.repo_path, d)
            os.makedirs(path, exist_ok=True)


    def _ensure_branches(self):
        """Créer les branches master et moderation si elles n'existent pas"""
        result = subprocess.run(
            ["git", "-C", self.repo_path, "branch"],
            capture_output=True, text=True
        )
        existing_branches = [b.strip("* ").strip() for b in result.stdout.splitlines()]
        for branch in self.DEFAULT_BRANCHES:
            if branch not in existing_branches:
                subprocess.run(["git", "-C", self.repo_path, "checkout", "-b", branch], check=True)

        # Toujours revenir sur master
        subprocess.run(["git", "-C", self.repo_path, "checkout", "master"], check=True)


    # -----------------------------
    # UPLOAD → a_moderer
    # -----------------------------
    def add_file_for_moderation(self, filename: str, content: bytes):
        """Ajouter un fichier dans a_moderer et commit sur moderation"""
        moderation_branch = "moderation"
        subprocess.run(["git", "-C", self.repo_path, "checkout", moderation_branch], check=True)

        path = os.path.join(self.repo_path, "a_moderer", filename)
        with open(path, "wb") as f:
            f.write(content)

        subprocess.run(["git", "-C", self.repo_path, "add", path], check=True)
        subprocess.run(["git", "-C", self.repo_path, "commit", "-m", f"Ajout {filename} pour modération"], check=True)


    # -----------------------------
    # LISTING
    # -----------------------------
    def list_moderation_files(self) -> List[str]:
        """Liste des fichiers à modérer"""
        moderation_branch = "moderation"
        subprocess.run(["git", "-C", self.repo_path, "checkout", moderation_branch], check=True)
        folder = os.path.join(self.repo_path, "a_moderer")
        os.makedirs(folder, exist_ok=True)
        return sorted(os.listdir(folder))

    def list_fond_commun_files(self) -> List[str]:
        """Liste des fichiers disponibles dans fond_commun sur master"""
        master_branch = "master"
        subprocess.run(["git", "-C", self.repo_path, "checkout", master_branch], check=True)
        folder = os.path.join(self.repo_path, "fond_commun")
        os.makedirs(folder, exist_ok=True)
        return sorted(os.listdir(folder))


    # -----------------------------
    # APPROUVER → fond_commun
    # -----------------------------
    def approve_file(self, filename: str):
        """
        Déplace un fichier de a_moderer (branch moderation)
        vers fond_commun (branch master) et commit.
        """
        moderation_branch = "moderation"
        master_branch = "master"
        # 1️⃣ Se placer sur moderation et récupérer le fichier
        subprocess.run(["git", "-C", self.repo_path, "checkout", moderation_branch], check=True)
        src_path = os.path.join(self.repo_path, "a_moderer", filename)
        if not os.path.exists(src_path):
            raise FileNotFoundError(f"{filename} introuvable dans {moderation_branch}")
        # 2️⃣ Copier le fichier dans master/fond_commun
        subprocess.run(["git", "-C", self.repo_path, "checkout", master_branch], check=True)
        dst_folder = os.path.join(self.repo_path, "fond_commun")
        os.makedirs(dst_folder, exist_ok=True)
        dst_path = os.path.join(dst_folder, filename)
        # Copier le fichier depuis la branche moderation via git show
        with open(dst_path, "wb") as f:
            subprocess.run(
                ["git", "-C", self.repo_path, "show", f"{moderation_branch}:a_moderer/{filename}"],
                check=True, stdout=f
            )

        # Commit sur master
        subprocess.run(["git", "-C", self.repo_path, "add", dst_path], check=True)
        subprocess.run(["git", "-C", self.repo_path, "commit", "-m",
                        f"Validation et ajout de {filename} au fond commun"], check=True)

        # 3️⃣ Supprimer le fichier de la branche moderation
        subprocess.run(["git", "-C", self.repo_path, "checkout", moderation_branch], check=True)
        os.remove(src_path)
        subprocess.run(["git", "-C", self.repo_path, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.repo_path, "commit", "-m", f"Retrait de {filename} de la modération"], check=True)

    # -----------------------------
    # REFUSER → supprimer
    # -----------------------------
    def reject_file(self, filename: str):
        """Supprimer un fichier de a_moderer et commit sur moderation"""
        moderation_branch = "moderation"
        subprocess.run(["git", "-C", self.repo_path, "checkout", moderation_branch], check=True)

        path = os.path.join(self.repo_path, "a_moderer", filename)
        if os.path.exists(path):
            os.remove(path)
            subprocess.run(["git", "-C", self.repo_path, "add", "-A"], check=True)
            subprocess.run(["git", "-C", self.repo_path, "commit", "-m", f"Rejet de {filename}"], check=True)
