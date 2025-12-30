from pyramid.view import view_config
from ..models import Session, Oeuvre, Utilisateurs, Proposition
from pyramid.httpexceptions import HTTPFound
from sqlalchemy.exc import IntegrityError
import tempfile
import os


# --- Page d'accueil ---
@view_config(route_name='home', renderer='app:templates/base.pt')
def home_view(request):
    main_content_html = """
    <div class="p-5 mb-4 bg-light rounded-3">
      <div class="container-fluid py-5">
        <h1 class="display-5 fw-bold">Bienvenue dans Ma Bibliothèque !</h1>
        <p class="col-md-8 fs-4">Profitez de notre catalogue et ajoutez des oeuvres.</p>
        <a class="btn btn-primary btn-lg" href="/oeuvres" role="button">Voir les oeuvres</a>
      </div>
    </div>
    """
    navbar_links = [
        ("Accueil", "/"),
        ("Oeuvres", "/oeuvres")
    ]
    
    if request.session.get("username"):
        navbar_links.append(("Proposer une oeuvre", '/upload'))
        
        if request.session.get("role") == "bibliothecaire":
            navbar_links.append(("Gestion bibliothécaire", "/gestion_biblio"))

        navbar_links.append(("Se déconnecter", "/logout"))
    else:
        navbar_links.append(("Se connecter", "/connect"))

    return {
        "title": "Accueil",
        "navbar_links": navbar_links,
        "main_content": main_content_html,
    }

# --- Page Oeuvres ---
@view_config(route_name='oeuvres', renderer='app:templates/base.pt')
def oeuvres_view(request):
    session = Session()
    oeuvres = session.query(Oeuvre).all()
    session.close()

    # Générer le HTML Bootstrap pour les œuvres
    main_content_html = "<h2>Liste des Oeuvres</h2><ul class='list-group'>"
    for o in oeuvres:
        main_content_html += f"""
        <li class='list-group-item'>{o.titre} - {o.auteur} ({o.annee}) <a class="btn btn-info" href="{request.route_url('apercu_oeuvre', id=o.id)}">Aperçu</a></li>
        """
    main_content_html += "</ul>"

    navbar_links = [
        ("Accueil", "/"),
        ("Oeuvres", "/oeuvres")
    ]
    
    if request.session.get("username"):
        navbar_links.append(("Proposer une oeuvre", '/upload'))
        
        if request.session.get("role") == "bibliothecaire":
            navbar_links.append(("Gestion bibliothécaire", "/gestion_biblio"))

        navbar_links.append(("Se déconnecter", "/logout"))
    else:
        navbar_links.append(("Se connecter", "/connect"))

    return {
        "title": "Oeuvres",
        "navbar_links": navbar_links,
        "main_content": main_content_html,
    }

# --- Page Membres ---

@view_config(route_name='connect', renderer='app:templates/base.pt')
def connect_view(request):
    form_type = request.params.get('form', 'connexion')
    session = Session()
    message = ""

    if request.method == 'POST':
        
        if "username" in request.params:
            username = request.params.get("username")
            password = request.params.get("password")

            from sqlalchemy import func

            user = session.query(Utilisateurs)\
                .filter(func.lower(Utilisateurs.username) == username.lower())\
                .first()


            if user and user.check_password(password):
                request.session["user_id"] = user.id
                request.session["username"] = user.username
                request.session["role"] = user.role
                return HTTPFound(location=request.route_url('home'))
            else:
                message = "Nom d'utilisateur ou mot de passe incorrect"
                form_type = "connexion"

        elif "new_username" in request.params:
            username = request.params.get("new_username")
            email = request.params.get("new_email")
            password = request.params.get("new_password")

            new_user = Utilisateurs(
                username=username,
                email=email,
                role="membre"
            )
            new_user.set_password(password)

            session.add(new_user)

            try:
                session.commit()
                return HTTPFound(location="/membres?form=connexion")
            except IntegrityError:
                session.rollback()
                message = "Nom d'utilisateur ou email déjà utilisé"
                form_type = "inscription"

    if form_type == "connexion":
        main_content_html = f"""
        <div class="d-flex justify-content-center mt-5">
          <div class="card shadow-sm" style="width: 400px;">
            <div class="card-body">
              <h2 class="card-title text-center mb-4">Connexion</h2>

              <div class="text-danger text-center mb-2">{message}</div>

              <form method="POST">
                <div class="mb-3">
                  <label class="form-label">Nom d'utilisateur</label>
                  <input type="text" class="form-control" name="username" required>
                </div>
                <div class="mb-3">
                  <label class="form-label">Mot de passe</label>
                  <input type="password" class="form-control" name="password" required>
                </div>
                <button type="submit" class="btn btn-primary w-100">Connexion</button>
              </form>

              <p class="text-center mt-3">
                Pas de compte ?
                <a href="/connect?form=inscription">S'inscrire</a>
              </p>
            </div>
          </div>
        </div>
        """
    else:
        main_content_html = f"""
        <div class="d-flex justify-content-center mt-5">
          <div class="card shadow-sm" style="width: 400px;">
            <div class="card-body">
              <h2 class="card-title text-center mb-4">Inscription</h2>

              <div class="text-danger mb-2">{message}</div>

              <form method="POST">
                <div class="mb-3">
                  <label class="form-label">Nom d'utilisateur</label>
                  <input type="text" class="form-control" name="new_username" required>
                </div>

                <div class="mb-3">
                  <label class="form-label">E-mail</label>
                  <input type="email" class="form-control" name="new_email" required>
                </div>

                <div class="mb-3">
                  <label class="form-label">Mot de passe</label>
                  <input type="password" class="form-control" name="new_password" required>
                </div>

                <button type="submit" class="btn btn-success w-100">Créer le compte</button>
              </form>

              <p class="text-center mt-3">
                Déjà inscrit ?
                <a href="/connect?form=connexion">Se connecter</a>
              </p>
            </div>
          </div>
        </div>
        """

    navbar_links = [
        ("Accueil", "/"),
        ("Oeuvres", "/oeuvres")
    ]
    
    if request.session.get("username"):
        navbar_links.append(("Proposer une oeuvre", '/upload'))
        
        if request.session.get("role") == "bibliothecaire":
            navbar_links.append(("Gestion bibliothécaire", "/gestion_biblio"))

        navbar_links.append(("Se déconnecter", "/logout"))
    else:
        navbar_links.append(("Se connecter", "/connect"))

    return {
        "title": "Se connecter",
        "navbar_links": navbar_links,
        "main_content": main_content_html,
    }
    
@view_config(route_name='logout')
def logout_view(request):
    # Supprime toutes les données de session
    request.session.invalidate()
    # Redirige vers la page d'accueil
    return HTTPFound(location=request.route_url('home'))


@view_config(route_name='upload', renderer='app:templates/base.pt')
def upload_view(request):
    import logging
    
    from ..ai_utils import (
        pdf_to_markdown_with_metadata,
        md_extract_metadata,
        ai_check_content
    )

    logger = logging.getLogger(__name__)

    session = Session()
    message = ""

    if request.method == "POST":
        fichier = request.params.get("fichier")

        if fichier is None or not fichier.filename:
            message = "Aucun fichier envoyé"
        else:
            filename = fichier.filename.lower()
            file_data = fichier.file.read()

            suffix = os.path.splitext(filename)[1]

            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(file_data)
                temp_path = tmp.name

            try:
                contenu_markdown = ""
                meta_info = {}

                if filename.endswith(".pdf"):
                    contenu_markdown, meta_info = pdf_to_markdown_with_metadata(temp_path)

                elif filename.endswith(".md"):
                    contenu_markdown, meta_info = md_extract_metadata(temp_path)

                else:
                    message = "Format de fichier non supporté"
                    raise ValueError(message)

                # --- Vérification contenu sécurisée ---
                if contenu_markdown.strip():
                    try:
                        est_explicite, libre_de_droit = ai_check_content(contenu_markdown)
                    except Exception as e:
                        logger.error(f"Impossible de vérifier le contenu: {e}")
                        est_explicite, libre_de_droit = False, True  # valeurs sûres par défaut
                else:
                    logger.warning("Le Markdown est vide, vérification de contenu ignorée")
                    est_explicite, libre_de_droit = False, True

                prop = Proposition(
                    titre=meta_info.get("titre", "Titre Inconnu"),
                    auteur=meta_info.get("auteur", "Inconnu"),
                    format_oeuvre="pdf" if filename.endswith(".pdf") else "md",
                    contenu_markdown=contenu_markdown,
                    meta_info=str(meta_info),
                    utilisateur_id=request.session.get("user_id"),
                    est_explicite=est_explicite,
                    libre_de_droit=libre_de_droit
                )

                session.add(prop)
                session.commit()

                return HTTPFound(
                    location=request.route_url("apercu_prop", id=prop.id)
                )

            finally:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
    
    main_content_html = f"""
    <div class="d-flex justify-content-center mt-5">
      <div class="card shadow-sm" style="width: 400px;">
        <div class="card-body">
          <h2 class="card-title text-center mb-4">Upload</h2>

          <div class="text-danger mb-2">{message}</div>

          <form method="POST" enctype="multipart/form-data">
            <div class="mb-3">
              <label class="form-label">Fichier PDF ou Markdown</label>
              <input type="file" name="fichier" accept=".pdf,.md" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-primary">Proposer l'oeuvre</button>
          </form>
        </div>
      </div>
    </div>
    """
    
    navbar_links = [
        ("Accueil", "/"),
        ("Oeuvres", "/oeuvres")
    ]
    
    if request.session.get("username"):
        navbar_links.append(("Proposer une oeuvre", '/upload'))
        
        if request.session.get("role") == "bibliothecaire":
            navbar_links.append(("Gestion bibliothécaire", "/gestion_biblio"))

        navbar_links.append(("Se déconnecter", "/logout"))
    else:
        navbar_links.append(("Se connecter", "/connect"))

    return {
        "title": "Proposer une oeuvre",
        "navbar_links": navbar_links,
        "main_content": main_content_html,
    }

@view_config(route_name='apercu_prop', renderer='app:templates/base.pt')
def apercu_prop_view(request):
    import markdown
    from markupsafe import Markup

    session = Session()
    prop_id = request.matchdict.get('id')
    prop = session.query(Proposition).get(prop_id)

    if not prop:
        session.close()
        return HTTPFound(location=request.route_url('home'))

    # Gestion des actions
    action = request.params.get('action')
    if action == 'annuler':
        session.delete(prop)
        session.commit()
        session.close()
        return HTTPFound(location=request.route_url('home'))
    elif action == 'envoyer':
        prop.est_valide = True
        session.commit()
        session.close()
        return HTTPFound(location=request.route_url('home'))

    # ===================================================
    # Filtrer le Markdown pour supprimer les notes de l'IA
    # ===================================================
    md_lines = (prop.contenu_markdown or "").splitlines()
    markdown_only = "\n".join(line for line in md_lines if not line.startswith("J’ai apporté les corrections"))

    # ===================================================
    # Conversion du Markdown en HTML
    # ===================================================
    html_content = Markup(markdown.markdown(
        markdown_only,
        extensions=[
            "extra",       # tables, définitions
            "fenced_code", # blocs de code ```python
            "toc",         # table des matières
            "sane_lists",  # listes améliorées
            "smarty"       # guillemets typographiques et tirets
        ]
    ))

    session.close()

    # ===================================================
    # HTML principal
    # ===================================================
    main_content_html = f"""
    <div class="container mt-4">
      <h2>{prop.titre}</h2>
      <p><strong>Auteur:</strong> {prop.auteur}</p>
      <p><strong>Format:</strong> {prop.format_oeuvre}</p>
      <hr/>
      <div class="markdown-preview">
        {html_content}  <!-- HTML sûr -->
      </div>
      <div class="mt-3">
        <form method="post">
          <button class="btn btn-secondary" name="action" value="annuler">Annuler</button>
          <button class="btn btn-success" name="action" value="envoyer">Envoyer aux bibliothécaires</button>
        </form>
      </div>
    </div>
    """

    # ===================================================
    # Barre de navigation
    # ===================================================
    navbar_links = [
        ("Accueil", "/"),
        ("Oeuvres", "/oeuvres")
    ]
    
    if request.session.get("username"):
        navbar_links.append(("Proposer une oeuvre", '/upload'))

        if request.session.get("role") == "bibliothecaire":
            navbar_links.append(("Gestion bibliothécaire", "/gestion_biblio"))

        navbar_links.append(("Se déconnecter", "/logout"))
    else:
        navbar_links.append(("Se connecter", "/connect"))

    return {
        "title": "Aperçu Proposition",
        "navbar_links": navbar_links,
        "main_content": main_content_html,
    }

@view_config(route_name="apercu_oeuvre", renderer="app:templates/base.pt")
def apercu_oeuvre_view(request):
    import markdown

    session = Session()
    oeuvre_id = request.matchdict.get('id')
    oeuvre = session.query(Oeuvre).get(oeuvre_id)

    html_content = markdown.markdown(
        oeuvre.contenu_markdown or "",
        extensions=[
            "extra",         # Tables, définitions, etc.
            "fenced_code",   # Blocs de code ```python
            "toc",           # Table des matières (utile si tu veux générer un sommaire)
            "sane_lists",    # Listes mieux formatées
            "smarty"         # Guillemets typographiques et tirets améliorés
        ]
    )

    session.close()

    main_content_html = f"""
    <div class="container mt-4">
      <h2>{oeuvre.titre}</h2>
      <p><strong>Auteur:</strong> {oeuvre.auteur}</p>
      <p><strong>Format:</strong> {oeuvre.format_oeuvre}</p>
      <hr/>
      <div class="markdown-preview">
        {html_content}  <!-- à transformer en HTML si tu utilises Markdown -->
      </div>
    </div>
    """

    navbar_links = [
        ("Accueil", "/"),
        ("Oeuvres", "/oeuvres")
    ]
    
    if request.session.get("username"):
        navbar_links.append(("Proposer une oeuvre", '/upload'))

        if request.session.get("role") == "bibliothecaire":
            navbar_links.append(("Gestion bibliothécaire", "/gestion_biblio"))

        navbar_links.append(("Se déconnecter", "/logout"))
    else:
        navbar_links.append(("Se connecter", "/connect"))

    return {
        "title": "Aperçu Oeuvre",
        "navbar_links": navbar_links,
        "main_content": main_content_html,
    }


@view_config(route_name="gestion_biblio", renderer="app:templates/base.pt")
def gestion_biblio_view(request):
    import logging
    from pyramid.httpexceptions import HTTPFound

    logger = logging.getLogger(__name__)
    session = Session()

    # Actions POST : validation ou rejet
    if request.method == "POST":
        prop_id = request.POST.get("prop_id")
        action = request.POST.get("action")
        proposition = session.query(Proposition).get(prop_id)
        
        if proposition:
            if action == "valider":
                # Créer une nouvelle Oeuvre avec tous les champs nécessaires
                oeuvre = Oeuvre(
                    titre=proposition.titre,
                    auteur=proposition.auteur,
                    annee=proposition.meta.get("annee") if proposition.meta else None,
                    contenu_markdown=proposition.contenu_markdown,
                    format_oeuvre=proposition.format_oeuvre,
                    est_explicite=proposition.est_explicite,
                    libre_de_droit=proposition.libre_de_droit,
                    utilisateur_id=proposition.utilisateur_id,
                    date_creation=proposition.date_creation
                )
                session.add(oeuvre)
                session.delete(proposition)  # Supprime la proposition après validation
                session.commit()
                logger.info(f"Proposition {prop_id} validée et transformée en oeuvre.")
            elif action == "rejeter":
                session.delete(proposition)
                session.commit()
                logger.info(f"Proposition {prop_id} rejetée et supprimée.")
        return HTTPFound(location=request.route_url("gestion_biblio"))

    # GET : afficher la liste des propositions
    propositions = session.query(Proposition).all()
    session.close()

    # Construire le HTML pour la liste
    main_content_html = ""
    for prop in propositions:
        main_content_html += f"""
        <div class="card mb-3">
            <div class="card-body">
                <h5 class="card-title">{prop.titre}</h5>
                <p class="card-text"><strong>Auteur:</strong> {prop.auteur}</p>
                <p class="card-text"><strong>Format:</strong> {prop.format_oeuvre}</p>
                <a class="btn btn-info" href="{request.route_url('apercu_prop', id=prop.id)}">Aperçu</a>
                <form method="post" style="display:inline;">
                    <input type="hidden" name="prop_id" value="{prop.id}">
                    <button type="submit" name="action" value="valider" class="btn btn-success">Valider</button>
                    <button type="submit" name="action" value="rejeter" class="btn btn-danger">Rejeter</button>
                </form>
            </div>
        </div>
        """

    navbar_links = [
        ("Accueil", "/"),
        ("Oeuvres", "/oeuvres")
    ]
    
    if request.session.get("username"):
        navbar_links.append(("Proposer une oeuvre", '/upload'))

        if request.session.get("role") == "bibliothecaire":
            navbar_links.append(("Gestion bibliothécaire", "/gestion_biblio"))

        navbar_links.append(("Se déconnecter", "/logout"))
    else:
        navbar_links.append(("Se connecter", "/connect"))

    return {
        "title": "Gestion Bibliothécaire",
        "navbar_links": navbar_links,
        "main_content": main_content_html,
    }

