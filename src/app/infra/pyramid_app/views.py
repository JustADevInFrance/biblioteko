from pyramid.view import view_config

repo_path = "~/bibliotheko_repo"
from app.domain.services.git_services import GitService

git_service = GitService(repo_path)

@view_config(route_name="home", renderer="templates/home.pt")
def home(request):
    """Page d'accueil de la bibliothèque."""
    return {
        "title": "Bienvenue dans Biblioteko",
        "message": "Bibliothèque numérique avec Pyramid + TAL/METAL",
        "features": ["Upload de documents", "Modération", "OCR IA", "Partage Git"]
    }

@view_config(route_name="moderation", renderer="templates/moderation.pt")
def moderation(request):
    """Page pour modérer les documents proposés par les membres."""
    return {"title": "Modération des documents"}



@view_config(route_name="upload", renderer="templates/upload.pt")
def upload(request):
    if request.method == "POST":
        file_storage = request.POST['file'].file
        filename = request.POST['file'].filename
        path = f"{repo_path}/{filename}"

        # Sauvegarde du fichier sur disque
        with open(path, "wb") as f:
            f.write(file_storage.read())

        # Commit dans Git
        git_service.add_file(filename, f"Ajout du fichier {filename}")

        message = f"Fichier {filename} ajouté avec succès."
        return {"title": "Uploader", "message": message}
    
    return {"title": "Uploader", "message": "Choisissez un fichier à envoyer"}