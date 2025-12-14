
import os
import markdown
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from domain.services.git_services import GitService
from domain.services.pdf_to_md import pdf_to_markdown

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
    features = [
        {"name": "Upload", "route": "upload"},
        {"name": "Modération", "route": "moderation"},
        {"name": "Fond commun", "route": "fond_commun"},
    ]

    return {
        "title": "Bienvenue dans Biblioteko",
        "message": "Bibliothèque numérique décentralisée",
        "features": features,
        "request": request,  # important pour route_url
    }



@view_config(route_name="upload", renderer="templates/upload.pt")
def upload(request):
    message = "Choisissez un fichier à envoyer"

    if request.method == "POST":
        uploaded_file = request.POST['file']  # <- ne pas utiliser get()
        if uploaded_file is None:
            message = "Aucun fichier reçu."
        else:
            # Vérification du type
            if hasattr(uploaded_file, 'filename'):
                filename = uploaded_file.filename
                file_bytes = uploaded_file.file.read()  # contenu binaire

                # Traiter le fichier (PDF → Markdown ou MD direct)
                ext = os.path.splitext(filename)[1].lower()
                if ext == ".md":
                    git_service.add_file_for_moderation(filename, file_bytes)
                    message = f"Fichier {filename} ajouté pour modération."
                elif ext == ".pdf":
                    tmp_pdf_path = os.path.join("/tmp", filename)
                    with open(tmp_pdf_path, "wb") as f:
                        f.write(file_bytes)

                    md_path = pdf_to_markdown(tmp_pdf_path, nombre_de_page=10)
                    with open(md_path, "rb") as f:
                        md_bytes = f.read()
                    git_service.add_file_for_moderation(os.path.basename(md_path), md_bytes)
                    os.remove(tmp_pdf_path)
                    message = f"{filename} converti en Markdown et ajouté pour modération."
                else:
                    message = "Format de fichier non supporté."
            else:
                message = "Fichier mal reçu."

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


@view_config(route_name="moderation_view",renderer="templates/fond_commun_view.pt")
def moderation_view(request):
    filename = request.matchdict["filename"]
    path = os.path.join(repo_path, "a_moderer", filename)

    if not os.path.exists(path):
        return Response("Fichier introuvable.", status=404)

    ext = os.path.splitext(filename)[1].lower()

    if ext == ".pdf":
        return Response(
            content_type="application/pdf",
            body=open(path, "rb").read()
        )

    if ext == ".md":
        with open(path, "r", encoding="utf-8") as f:
            md_text = f.read()

        html = markdown.markdown(md_text)

        return {
            "title": filename,
            "content": html
        }

    return Response("Format non supporté", status=400)



# -----------------------------
# APPROUVER
# -----------------------------
@view_config(route_name="moderation_approve")
def moderation_approve(request):
    filename = request.matchdict["filename"]
    git_service.approve_file(filename)
    return HTTPFound(location=request.route_url("moderation"))



# -----------------------------
# REFUSER
# -----------------------------
@view_config(route_name="moderation_reject")
def moderation_reject(request):
    filename = request.matchdict["filename"]
    git_service.reject_file(filename)
    return HTTPFound(location=request.route_url("moderation"))

# -----------------------------
# PAGE FOND COMMUN
# -----------------------------

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


@view_config(route_name="fond_commun_view", renderer="templates/fond_commun_view.pt")
def fond_commun_view(request):
    """Afficher un fichier du fond commun, Markdown en HTML si possible."""
    filename = request.matchdict["filename"]
    path = os.path.join(git_service.repo_path, "fond_commun", filename)

    if not os.path.exists(path):
        return Response("Fichier introuvable.", status=404)

    ext = os.path.splitext(filename)[1].lower()

    if ext == ".md":
        with open(path, "r", encoding="utf-8") as f:
            md_content = f.read()
        html_content = markdown.markdown(md_content)
        return {
            "title": filename,
            "content": html_content
        }
    else:
        # Pour PDF ou autres → téléchargement direct
        mime_type, _ = mimetypes.guess_type(path)
        return Response(
            content_type=mime_type or "application/octet-stream",
            body=open(path, "rb").read(),
            content_disposition=f'attachment; filename="{escape(filename)}"'
        )
