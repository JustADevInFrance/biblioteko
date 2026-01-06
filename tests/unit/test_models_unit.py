from app.models import Utilisateurs, Oeuvre, Proposition

# -------------------------
# Utilisateurs
# -------------------------
def test_set_and_check_password():
    user = Utilisateurs(username="testuser", email="t@test.com")
    user.set_password("secret")
    assert user.password_hash is not None
    assert user.check_password("secret")
    assert not user.check_password("wrongpassword")

def test_user_role_default():
    user = Utilisateurs(username="testuser2", email="t@test.com")
    assert user.role == "membre"

def test_user_role_assignment():
    admin_user = Utilisateurs(username="admin", email="admin@test.com", role="admin")
    assert admin_user.role == "admin"

def test_username_case_insensitivity():
    user = Utilisateurs(username="CaseTest", email="")
    user.set_password("password")
    assert user.check_password("password")

# -------------------------
# Oeuvre
# -------------------------
def test_oeuvres_attributes():
    oeuvre = Oeuvre(
        titre="Test Oeuvre",
        auteur="Auteur Test",
        format_oeuvre="pdf",
        contenu_markdown="Ceci est un test."
    )
    assert oeuvre.titre == "Test Oeuvre"
    assert oeuvre.auteur == "Auteur Test"
    assert oeuvre.format_oeuvre == "pdf"
    assert oeuvre.contenu_markdown == "Ceci est un test."
    assert oeuvre.id is None
    assert oeuvre.date_creation is not None
    assert oeuvre.est_explicite is False
    assert oeuvre.libre_de_droit is True

# -------------------------
# Proposition
# -------------------------
def test_proposition_attributes():
    proposition = Proposition(
        titre="Proposition Test",
        auteur="Auteur Prop",
        format_oeuvre="pdf",
        contenu_markdown="Contenu de la proposition."
    )
    assert proposition.titre == "Proposition Test"
    assert proposition.auteur == "Auteur Prop"
    assert proposition.format_oeuvre == "pdf"
    assert proposition.contenu_markdown == "Contenu de la proposition."
    assert proposition.id is None
    assert proposition.date_creation is not None
    assert proposition.est_valide is False
    assert proposition.est_explicite is False
    assert proposition.libre_de_droit is False
