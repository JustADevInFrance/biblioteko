import pytest
from webtest import TestApp
from app import main
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, DBSession


@pytest.fixture(scope="function")
def engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture(scope="function")
def db_session(engine):
    """
    Session SQLAlchemy partagée avec l’app
    """
    connection = engine.connect()
    transaction = connection.begin()

    Session = sessionmaker(bind=connection)
    session = Session()

    DBSession.configure(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def test_app(engine):
    """
    Application Pyramid complète branchée sur la même DB
    """
    settings = {
        "sqlalchemy.url": "sqlite:///:memory:"
    }

    app = main({}, **settings)
    return TestApp(app)
