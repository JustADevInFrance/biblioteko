import pytest
from pyramid.httpexceptions import HTTPFound
from unittest.mock import patch, MagicMock

from app.models import Utilisateurs, Oeuvre, Proposition, DemandeRole
from app.views.home import (
    home_view,
    connect_view,
    logout_view,
    upload_view,
    apercu_prop_view,
    apercu_oeuvre_view,
    gestion_biblio_view,
    demande_role_view,
    admin_refuser,
    admin_demandes_view,
    admin_accepter
)

# ===========================
# Home View
# ===========================
def test_home_view_logged_out(dummy_request):
    dummy_request.session = {}
    dummy_request.route_url = lambda route, **kw: f"/{route}"
    response = home_view(dummy_request)
    assert response["title"] == "Accueil"
    assert any(label.lower() == "se connecter" for label, _ in response["navbar_links"])

def test_home_view_logged_in(dummy_request, db_session):
    user = Utilisateurs(username="user1", email="u1@test.com")
    user.set_password("pwd")
    db_session.add(user)
    db_session.commit()
    dummy_request.session = {"username": "user1", "role": "membre"}
    dummy_request.route_url = lambda route, **kw: f"/{route}"
    response = home_view(dummy_request)
    assert any("proposer" in label.lower() for label, _ in response["navbar_links"])

# ===========================
# Connect View
# ===========================
def test_connect_view_login_success(dummy_request, db_session):
    user = Utilisateurs(username="Alice", email="alice@test.com")
    user.set_password("password123")
    db_session.add(user)
    db_session.commit()

    dummy_request.method = "POST"
    dummy_request.params = {"username": "Alice", "password": "password123"}
    dummy_request.session = {}
    dummy_request.route_url = lambda route, **kw: f"/{route}"

    from app.views.home import Session
    with patch("app.views.home.Session", return_value=db_session):
        response = connect_view(dummy_request)

    assert isinstance(response, HTTPFound)
    assert dummy_request.session["username"].lower() == "alice"
    assert dummy_request.session["role"] == "membre"

def test_connect_view_login_failure(dummy_request, db_session):
    user = Utilisateurs(username="Bob", email="bob@test.com")
    user.set_password("securepwd")
    db_session.add(user)
    db_session.commit()

    dummy_request.method = "POST"
    dummy_request.params = {"username": "Bob", "password": "wrongpwd"}
    dummy_request.session = {}
    dummy_request.route_url = lambda route, **kw: f"/{route}"

    from app.views.home import Session
    with patch("app.views.home.Session", return_value=db_session):
        response = connect_view(dummy_request)

    # Devrait renvoyer la page connexion
    assert "main_content" in response
    assert "username" not in dummy_request.session

def test_connect_view_registration_success(dummy_request, db_session):
    dummy_request.method = "POST"
    dummy_request.params = {"new_username": "Charlie", "new_email": "charlie@test.com", "new_password": "charliepwd"}
    dummy_request.session = {}
    dummy_request.route_url = lambda route, **kw: f"/{route}"

    from app.views.home import Session
    with patch("app.views.home.Session", return_value=db_session):
        response = connect_view(dummy_request)

    user = db_session.query(Utilisateurs).filter_by(username="Charlie").first()
    assert isinstance(response, HTTPFound)
    assert user is not None
    assert user.check_password("charliepwd")

def test_connect_view_registration_failure_existing_username(dummy_request, db_session):
    existing_user = Utilisateurs(username="Dave", email="dave@test.com")
    existing_user.set_password("pwd")
    db_session.add(existing_user)
    db_session.commit()

    dummy_request.method = "POST"
    dummy_request.params = {"new_username": "Dave", "new_email": "dave2@test.com", "new_password": "pwd2"}
    dummy_request.session = {}
    dummy_request.route_url = lambda route, **kw: f"/{route}"

    from app.views.home import Session
    with patch("app.views.home.Session", return_value=db_session):
        response = connect_view(dummy_request)

    assert "main_content" in response
    assert "déjà utilisé" in response["main_content"]

# ===========================
# Logout View
# ===========================
def test_logout_view(dummy_request):
    class DummySession(dict):
        def invalidate(self):
            self.clear()
    dummy_request.session = DummySession({"username": "test"})
    dummy_request.route_url = lambda route: "/"
    response = logout_view(dummy_request)
    assert isinstance(response, HTTPFound)
    assert not dummy_request.session

# ===========================
# Upload View
# ===========================
def test_upload_view_get(dummy_request):
    dummy_request.method = "GET"
    dummy_request.session = {"user_id": 1}
    dummy_request.route_url = lambda route, **kw: f"/{route}"
    response = upload_view(dummy_request)
    assert response["title"] == "Proposer une oeuvre"
    assert "form" in response["main_content"]

def test_upload_view_post_success(dummy_request, db_session):
    dummy_request.method = "POST"
    dummy_request.session = {"user_id": 1}
    dummy_request.params = {"fichier": "fake.pdf"}
    dummy_request.route_url = lambda route, **kw: f"/apercu_prop/{kw.get('id')}"

    fake_prop = Proposition(titre="Fake", auteur="Author", format_oeuvre="pdf", contenu_markdown="Contenu")
    with patch("app.views.home.handle_upload", return_value=fake_prop):
        response = upload_view(dummy_request)

    assert isinstance(response, HTTPFound)
    assert str(fake_prop.id) in response.location

# ===========================
# Aperçu Proposition View
# ===========================
def test_apercu_prop_view_actions(dummy_request, db_session):
    prop = Proposition(titre="TestProp", auteur="Author", format_oeuvre="pdf", contenu_markdown="Contenu")
    db_session.add(prop)
    db_session.commit()
    dummy_request.matchdict = {"id": prop.id}
    dummy_request.params = {"action": "envoyer"}
    dummy_request.session = {"user_id": 1}
    dummy_request.route_url = lambda route, **kw: "/"
    response = apercu_prop_view(dummy_request)
    assert isinstance(response, HTTPFound)

# ===========================
# Aperçu Oeuvre View
# ===========================
def test_apercu_oeuvre_view(dummy_request, db_session):
    oeuvre = Oeuvre(titre="TestOeuvre", auteur="Author", format_oeuvre="pdf", contenu_markdown="Contenu")
    db_session.add(oeuvre)
    db_session.commit()
    dummy_request.matchdict = {"id": oeuvre.id}
    dummy_request.session = {"user_id": 1}
    dummy_request.route_url = lambda route, **kw: "/"
    response = apercu_oeuvre_view(dummy_request)
    assert isinstance(response, dict) or isinstance(response, HTTPFound)

# ===========================
# Gestion Bibliothécaire View
# ===========================
def test_gestion_biblio_view_get(dummy_request, db_session):
    dummy_request.method = "GET"
    dummy_request.session = {"user_id": 1}
    dummy_request.route_url = lambda route, **kw: "/"
    db_session.add(Proposition(titre="Prop1", auteur="Author", format_oeuvre="pdf", contenu_markdown="Contenu"))
    db_session.commit()
    response = gestion_biblio_view(dummy_request)
    assert response["title"] == "Gestion Bibliothécaire"

# ===========================
# Demande Role View
# ===========================
def test_demande_role_view_post(dummy_request, db_session):
    user = Utilisateurs(username="user2", email="u2@test.com")
    user.set_password("pwd")
    db_session.add(user)
    db_session.commit()

    dummy_request.session = {"username": "user2"}
    dummy_request.method = "POST"
    dummy_request.route_url = lambda route, **kw: "/"

    from app.views.home import Session
    with patch("app.views.home.Session", return_value=db_session):
        response = demande_role_view(dummy_request)

    assert "main_content" in response
    assert "Demande envoyée" in response["main_content"]

# ===========================
# Admin Views
# ===========================
def test_admin_demandes_view_access_denied(dummy_request):
    dummy_request.session = {"role": "membre"}
    dummy_request.route_url = lambda route, **kw: "/"
    response = admin_demandes_view(dummy_request)
    assert isinstance(response, HTTPFound)

def test_admin_refuser_and_accepter(dummy_request, db_session, admin_user):
    demande = DemandeRole(utilisateur_id=admin_user.id)
    db_session.add(demande)
    db_session.commit()

    dummy_request.session = {"role": "admin"}
    dummy_request.matchdict = {"id": demande.id}
    dummy_request.route_url = lambda route, **kw: "/"

    resp_refuse = admin_refuser(dummy_request)
    assert isinstance(resp_refuse, HTTPFound)

    # recréer la demande pour accepter
    demande2 = DemandeRole(utilisateur_id=admin_user.id)
    db_session.add(demande2)
    db_session.commit()
    dummy_request.matchdict = {"id": demande2.id}
    resp_accept = admin_accepter(dummy_request)
    assert isinstance(resp_accept, HTTPFound)
