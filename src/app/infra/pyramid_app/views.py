
import os
from pyramid.view import view_config
from pyramid.response import Response
from domain.services.git_services import GitService

import mimetypes


# 🔹 PATH du dépôt Git (créé dans Docker)
repo_path = os.getenv("PYRAMID_REPO_PATH", "/app/git_data")

# 🔹 Instance Git
git_service = GitService(repo_path)


# -----------------------------
# PAGE D'ACCUEIL
# -----------------------------
@view_config(route_name="home", renderer="templates/home.pt")
def home(request):
    return {
        "title": "Bienvenue dans Biblioteko",
        "message": "Bibliothèque numérique décentralisée",
        "features": ["Upload", "Modération", "Git", "TAL/METAL"]
    }


# -----------------------------
# UPLOAD UTILISATEUR
# -----------------------------
@view_config(route_name="upload", renderer="templates/upload.pt")
def upload(request):
    message = "Choisissez un fichier à envoyer"

    if request.method == "POST":
        uploaded_file = request.POST.get("file")
        if uploaded_file is None:
            message = "Aucun fichier reçu."
        else:
            filename = uploaded_file.filename
            file_bytes = uploaded_file.file.read()
            # Ajout dans Git → a_moderer/
            git_service.add_file_for_moderation(filename, file_bytes)
            message = f"Fichier {filename} ajouté pour modération."

    return {"title": "Uploader", "message": message}





# -----------------------------
# PAGE DE MODÉRATION
# -----------------------------
@view_config(route_name="moderation", renderer="templates/moderation.pt")
def moderation(request):
    """
    Page pour modérer les fichiers proposés par les utilisateurs.
    Affiche la liste des fichiers en attente de validation et un message optionnel.
    """
    files = git_service.list_moderation_files()

    # Si aucun fichier à modérer, on peut afficher un message
    if not files:
        message = "Aucun fichier à modérer pour l'instant."
    else:
        message = None  # Pas de message si des fichiers existent

    return {
        "title": "Modération des documents",
        "files": files,
        "message": message
    }



# -----------------------------
# CONSULTER UN DOCUMENT
# -----------------------------
@view_config(route_name="moderation_view")
def moderation_view(request):
    filename = request.matchdict["filename"]
    path = os.path.join(repo_path, "a_moderer", filename)

    if not os.path.exists(path):
        return Response("Fichier introuvable.", status=404)

    return Response(
        content_type="application/pdf",
        body=open(path, "rb").read()
    )


# -----------------------------
# APPROUVER
# -----------------------------
@view_config(route_name="moderation_approve")
def moderation_approve(request):
    filename = request.matchdict["filename"]
    git_service.approve_file(filename)
    return Response(f"{filename} approuvé et déplacé dans fond_commun.")


# -----------------------------
# REFUSER
# -----------------------------
@view_config(route_name="moderation_reject")
def moderation_reject(request):
    filename = request.matchdict["filename"]
    git_service.reject_file(filename)
    return Response(f"{filename} rejeté et supprimé.")

@view_config(route_name="fond_commun", renderer="templates/fond_commun.pt")
def fond_commun(request):
    files = git_service.list_fond_commun_files()
    return {
        "title": "Fond Commun",
        "files": files
    }

@view_config(route_name="fond_commun", renderer="templates/fond_commun.pt")
def fond_commun(request):
    files = git_service.list_fond_commun_files()  # Méthode à créer pour lister les fichiers
    return {
        "title": "Fond Commun",
        "files": files,
        "message": None  # ou un message type "Aucun fichier" si nécessaire
    }



@view_config(route_name="fond_commun_download")
def fond_commun_download(request):
    filename = request.matchdict["filename"]
    path = os.path.join(git_service.repo_path, "fond_commun", filename)

    if not os.path.exists(path):
        return Response("Fichier introuvable.", status=404)

    mime_type, _ = mimetypes.guess_type(path)
    return Response(
        content_type=mime_type or "application/octet-stream",
        body=open(path, "rb").read()
    )
