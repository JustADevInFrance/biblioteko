import os
from pyramid.view import view_config

# Import du service Git depuis Domain (DDD)
from domain.services.git_services import GitService


# ---------------------------------------------------------------------
# CONFIGURATION DU RÉPERTOIRE GIT
# ---------------------------------------------------------------------
# Sous Docker, ce répertoire doit être monté comme volume :
# docker-compose :   ./git_data:/app/git_data
# Dockerfile :        WORKDIR /app
repo_path = os.getenv("PYRAMID_REPO_PATH", "/app/git_data")

# On s’assure que le répertoire existe
os.makedirs(repo_path, exist_ok=True)

# Instanciation du service Git
git_service = GitService(repo_path)



# ---------------------------------------------------------------------
# ⬤ PAGE D'ACCUEIL
# ---------------------------------------------------------------------
@view_config(route_name="home", renderer="templates/home.pt")
def home(request):
    """Page d'accueil de la bibliothèque numérique."""
    return {
        "title": "Bienvenue dans Biblioteko",
        "message": "Bibliothèque numérique avec Pyramid + TAL/METAL",
        "features": [
            "Upload de documents",
            "Modération",
            "Gestion Git",
            "Architecture DDD",
            "Compatibilité Docker"
        ]
    }

# ---------------------------------------------------------------------

@view_config(route_name="creation_de_compte", renderer="templates/creation_de_compte.pt")
def create_user_view(request):
    if request.method == "POST":
        prenom = request.POST['prenom']
        nom = request.POST['nom']
        email = request.POST['email']
        git_service.create_user(prenom, nom, email)
        return {"message": f"Utilisateur {prenom} {nom} créé avec succès"}
    return {}

# Upload d'un fichier
@view_config(route_name="upload", renderer="templates/upload.pt")
def upload_view(request):
    if request.method == "POST":
        username = request.POST.get('username')  # à adapter selon session
        file_storage = request.POST['file'].file
        filename = request.POST['file'].filename
        git_service.upload_user_file(username, filename, file_storage.read())
        return {"message": f"Fichier {filename} envoyé en modération"}
    return {}

# Page modération
@view_config(route_name="moderation", renderer="templates/moderation.pt")
def moderation_view(request):
    files = git_service.list_moderation_files()
    return {"moderation_files": files}

# Actions sur la modération
@view_config(route_name="moderation_action", request_method="POST")
def moderation_action(request):
    filename = request.POST['filename']
    action = request.POST['action']
    commentaire = request.POST.get('commentaire', "")
    if action == "valider":
        git_service.approve(filename)
    elif action == "refuser":
        git_service.reject(filename, commentaire)
    # consulter → à implémenter selon UI
    return {"moderation_files": git_service.list_moderation_files()}