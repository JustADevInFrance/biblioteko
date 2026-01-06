import pytest
from pyramid import testing
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Utilisateurs
from app import main
from webtest import TestApp

# =========================================================
# WSGI Test App
# =========================================================
@pytest.fixture(scope="function")
def test_app():
    """Retourne un WSGI test app pour integration."""
    settings = {}
    app = main({}, **settings)
    return TestApp(app)

# =========================================================
# DB session pour tests
# =========================================================
@pytest.fixture(scope="function")
def db_session():
    """Base de données SQLite en mémoire pour tests."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

# =========================================================
# Fixtures utilisateurs
# =========================================================
@pytest.fixture(scope="function")
def admin_user(db_session):
    user = Utilisateurs(username="admin", email="admin@test.com", role="admin")
    user.set_password("adminpass")
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture(scope="function")
def member_user(db_session):
    user = Utilisateurs(username="member", email="member@test.com", role="membre")
    user.set_password("pwd")
    db_session.add(user)
    db_session.commit()
    return user

# =========================================================
# DummyRequest Pyramid
# =========================================================
@pytest.fixture
def dummy_request():
    """Faux objet request Pyramid pour tests unitaires."""
    request = testing.DummyRequest()
    request.session = {}
    return request
