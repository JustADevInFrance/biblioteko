import pytest
from pyramid import testing
from app.models import Utilisateurs

# =========================================================
# DummyRequest Pyramid
# =========================================================
@pytest.fixture
def dummy_request():
    """
    Faux objet request Pyramid pour tests unitaires.
    """
    request = testing.DummyRequest()
    request.session = {}
    return request

# =========================================================
# Utilisateur membre fictif
# =========================================================
@pytest.fixture
def member_user():
    user = Utilisateurs(username="member", email="member@test.com", role="membre")
    user.set_password("pwd")
    return user

# =========================================================
# Utilisateur admin fictif
# =========================================================
@pytest.fixture
def admin_user():
    user = Utilisateurs(username="admin", email="admin@test.com", role="admin")
    user.set_password("adminpass")
    return user
