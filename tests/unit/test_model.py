from app.models import Utilisateurs, Oeuvre, Proposition

def test_create_user(db_session):
    user = Utilisateurs(username="testuser", email="test@test.com")
    user.set_password("secret")
    db_session.add(user)
    db_session.commit()

    u = db_session.query(Utilisateurs).filter_by(username="testuser").first()
    assert u is not None
    assert u.check_password("secret") is True
    assert u.role == "membre"

def test_create_oeuvre(db_session):
    oeuvre = Oeuvre(
        titre="Titre Test",
        auteur="Auteur Test",
        contenu_markdown="Contenu",
        format_oeuvre="pdf"
    )
    db_session.add(oeuvre)
    db_session.commit()

    o = db_session.query(Oeuvre).first()
    assert o.titre == "Titre Test"
    assert o.format_oeuvre == "pdf"

def test_proposition(db_session):
    prop = Proposition(
        titre="Prop Test",
        auteur="Auteur Test",
        contenu_markdown="Contenu",
        format_oeuvre="md"
    )
    db_session.add(prop)
    db_session.commit()
    p = db_session.query(Proposition).first()
    assert p.titre == "Prop Test"

