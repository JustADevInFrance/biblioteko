from app.views.home import home_view, connect_view, upload_view

def test_home_view_logged_out(dummy_request):
    dummy_request.session = {}
    response = home_view(dummy_request)
    assert "Accueil" in response["title"]
    assert any(link[0] == "Se connecter" for link in response["navbar_links"])

def test_home_view_logged_in(dummy_request, db_session):
    from app.models import Utilisateurs
    user = Utilisateurs(username="test", email="t@test.com")
    user.set_password("pwd")
    db_session.add(user)
    db_session.commit()

    dummy_request.session = {"username": "test", "role": "membre"}
    response = home_view(dummy_request)
    assert any(link[0] == "Proposer une oeuvre" for link in response["navbar_links"])

