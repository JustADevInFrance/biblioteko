from pyramid.view import view_config
from ..models import Session, Oeuvre, Utilisateurs, Proposition, DemandeRole
from pyramid.httpexceptions import HTTPFound
from sqlalchemy.exc import IntegrityError
import tempfile
import os
from sqlalchemy import func
from sqlalchemy.orm import joinedload

from .helpers import *
from .templates_fragments import *
from ..services.upload_service import *

def demande_en_cours(session, user_id):
    """Retourne True si l'utilisateur a déjà une demande en attente"""
    existante = session.query(DemandeRole).filter_by(
        utilisateur_id=user_id,
        statut="en_attente"
    ).first()
    return bool(existante)

# --- Page d'accueil ---
@view_config(route_name='home', renderer='app:templates/base.pt')
def home_view(request):
    return {
        "title": "Accueil",
        "navbar_links": build_navbar(request),
        "main_content": home_content(),
    }


@view_config(route_name='oeuvres', renderer='app:templates/base.pt')
def oeuvres_view(request):
    session = Session()
    oeuvres = session.query(Oeuvre).all()
    session.close()

    return {
        "title": "Oeuvres",
        "navbar_links": build_navbar(request),
        "main_content": oeuvres_content(oeuvres, request),
    }


@view_config(route_name='connect', renderer='app:templates/base.pt')
def connect_view(request):
    form_type = request.params.get('form', 'connexion')
    session = Session()
    message = ""

    # --- LOGIQUE POST ---
    if request.method == "POST":
        # --- Connexion ---
        if "username" in request.params:
            username = request.params.get("username")
            password = request.params.get("password")[:72]  # limitation bcrypt
            user = session.query(Utilisateurs)\
                .filter(func.lower(Utilisateurs.username) == username.lower())\
                .first()

            if user and user.check_password(password):
                request.session["user_id"] = user.id
                request.session["username"] = user.username
                request.session["role"] = user.role
                session.close()
                return HTTPFound(location=request.route_url('home'))
            else:
                message = "Nom d'utilisateur ou mot de passe incorrect"
                form_type = "connexion"

        # --- Inscription ---
        elif "new_username" in request.params:
            username = request.params.get("new_username")
            email = request.params.get("new_email")
            password = request.params.get("new_password")[:72]

            new_user = Utilisateurs(
                username=username,
                email=email,
                role="membre"
            )
            new_user.set_password(password)

            session.add(new_user)
            try:
                session.commit()
                session.close()
                return HTTPFound(location=request.route_url("connect", _query={"form":"connexion"}))
            except IntegrityError:
                session.rollback()
                message = "Nom d'utilisateur ou email déjà utilisé"
                form_type = "inscription"

    # --- BUILD MAIN CONTENT ---
    main_content = (
        connexion_form(message)
        if form_type == "connexion"
        else inscription_form(message)
    )

    session.close()
    return {
        "title": "Connexion",
        "navbar_links": build_navbar(request),
        "main_content": main_content,
    }


    
@view_config(route_name='logout')
def logout_view(request):
    # Supprime toutes les données de session
    request.session.invalidate()
    # Redirige vers la page d'accueil
    return HTTPFound(location=request.route_url('home'))


@view_config(route_name='upload', renderer='app:templates/base.pt')
def upload_view(request):

    session = Session()
    message = ""

    if request.method == "POST":
        try:
            prop = handle_upload(
                request.params.get("fichier"),
                request.session.get("user_id"),
                session
            )
            return HTTPFound(
                location=request.route_url("apercu_prop", id=prop.id)
            )
        except Exception as e:
            message = str(e)

    return {
        "title": "Proposer une oeuvre",
        "navbar_links": build_navbar(request),
        "main_content": upload_form(message),
    }


@view_config(route_name='apercu_prop', renderer='app:templates/base.pt')
def apercu_prop_view(request):

    session = Session()
    prop = session.get(Proposition, request.matchdict.get("id"))

    if not prop:
        session.close()
        return HTTPFound(location=request.route_url("home"))

    action = request.params.get("action")
    if action == "annuler":
        session.delete(prop)
        session.commit()
        session.close()
        return HTTPFound(location=request.route_url("home"))

    if action == "envoyer":
        prop.est_valide = True
        session.commit()
        session.close()
        return HTTPFound(location=request.route_url("home"))

    markdown_clean = clean_markdown(prop.contenu_markdown)
    html_content = markdown_to_html(markdown_clean)
    session.close()

    return {
        "title": "Aperçu Proposition",
        "navbar_links": build_navbar(request),
        "main_content": apercu_prop_content(prop, html_content),
    }


@view_config(route_name="apercu_oeuvre", renderer="app:templates/base.pt")
def apercu_oeuvre_view(request):

    session = Session()
    oeuvre = session.get(Oeuvre, request.matchdict.get("id"))
    session.close()

    if not oeuvre:
        return HTTPFound(location=request.route_url("oeuvres"))

    html_content = markdown_to_html(oeuvre.contenu_markdown)

    return {
        "title": "Aperçu Oeuvre",
        "navbar_links": build_navbar(request),
        "main_content": apercu_oeuvre_content(oeuvre, html_content),
    }



@view_config(route_name="gestion_biblio", renderer="app:templates/base.pt")
def gestion_biblio_view(request):
    session = Session()

    if request.method == "POST":
        prop_id = request.POST.get("prop_id")
        action = request.POST.get("action")

        proposition = session.get(Proposition, prop_id)
        if proposition:
            traiter_proposition(session, proposition, action)

        session.close()
        return HTTPFound(location=request.route_url("gestion_biblio"))

    propositions = session.query(Proposition).all()
    session.close()

    return {
        "title": "Gestion Bibliothécaire",
        "navbar_links": build_navbar(request),
        "main_content": gestion_biblio_content(propositions, request),
    }


@view_config(route_name="demande_role",renderer="app:templates/base.pt",request_method=["GET", "POST"])
def demande_role_view(request):

    if not request.session.get("username"):
        return HTTPFound(location="/connect")

    session = Session()
    user = session.query(Utilisateurs).filter_by(
        username=request.session["username"]
    ).first()

    message = ""

    if request.method == "POST":
        if demande_en_cours(session, user.id):
            message = "Une demande est déjà en cours."
        else:
            demande = DemandeRole(utilisateur_id=user.id)
            session.add(demande)
            session.commit()
            message = "Demande envoyée avec succès."


    session.close()

    return {
        "title": "Demande de rôle",
        "navbar_links": build_navbar(request),
        "main_content": demande_role_content(message),
    }


@view_config(route_name="admin_refuser")
def admin_refuser(request):
    if request.session.get("role") != "admin":
        return HTTPFound(location="/")

    session = Session()
    demande = session.get(DemandeRole, request.matchdict["id"])

    if demande:
        demande.statut = "refuse"
        demande.date_traitement = datetime.utcnow()
        # facultatif : stocker un motif
        demande.motif_refus = "Rejeté par l'administrateur"
        session.commit()

    session.close()
    return HTTPFound(location="/admin/demandes")


@view_config(route_name="admin_demandes", renderer="app:templates/base.pt")
def admin_demandes_view(request):
    
    if request.session.get("role") != "admin":
        return HTTPFound(location="/")

    session = Session()
    demandes = session.query(DemandeRole).options(joinedload(DemandeRole.utilisateur)).filter_by(statut="en_attente").all()
    session.close()

    return {
        "title": "Administration",
        "navbar_links": build_navbar(request),
        "main_content": admin_demandes_content(demandes, request),
    }


@view_config(route_name="admin_accepter")
def admin_accepter(request):
    from ..services.demande_role_service import accepter_demande

    if request.session.get("role") != "admin":
        return HTTPFound(location="/")

    session = Session()
    demande = session.get(DemandeRole, request.matchdict["id"])

    if demande:
        accepter_demande(session, demande)

    session.close()
    return HTTPFound(location="/admin/demandes")

