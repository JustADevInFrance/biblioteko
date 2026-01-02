def test_proposition_creation(test_app, db_session):
    # Créer un utilisateur
    from app.models import Utilisateurs
    user = Utilisateurs(username="user2", email="user2@test.com")
    user.set_password("secret")
    db_session.add(user)
    db_session.commit()

    # Simuler session utilisateur
    test_app.set_cookie("username", "user2")
    test_app.set_cookie("user_id", str(user.id))
    
    # POST fichier simulé
    import io
    file_content = io.BytesIO(b"Contenu markdown test")
    res = test_app.post("/upload", upload_files=[("fichier", "test.md", file_content.getvalue())])
    
    # Doit rediriger vers l’aperçu proposition
    assert res.status_code == 302
    assert "/proposition/" in res.location

