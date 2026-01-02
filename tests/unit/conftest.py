import pytest
from pyramid import testing
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Utilisateurs

from app import main  # ton main Pyramid

@pytest.fixture(scope="function")
def test_app():
    """Retourne un WSGI test app."""
    settings = {}
    app = main({}, **settings)
    from webtest import TestApp
    return TestApp(app)

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

@pytest.fixture(scope="function")
def create_admin(db_session):
    admin = Utilisateurs(username="admin", email="admin@test.com", role="admin")
    admin.set_password("adminpass")
    db_session.add(admin)
    db_session.commit()
    return admin

import pytest
from pyramid import testing

@pytest.fixture
def dummy_request():
    """
    Faux objet request Pyramid pour tests unitaires
    """
    request = testing.DummyRequest()
    request.session = {}
    return request
