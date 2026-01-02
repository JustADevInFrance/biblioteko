def test_connexion_membre(test_app, db_session):
    from app.models import Utilisateurs

    # Création utilisateur en base
    user = Utilisateurs(username="user1", email="user1@test.com")
    user.set_password("secret")
    db_session.add(user)
    db_session.commit()

    # Simulation POST /connect
    res = test_app.post("/connect", {
        "username": "user1",
        "password": "secret"
    })

    # Vérifier redirection vers home
    assert res.status_code == 302
    assert res.location.endswith("/")
