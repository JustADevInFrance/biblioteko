from pyramid.config import Configurator
from .routes import include_routes

def create_app():
    """Crée l'application Pyramid avec routes et vues."""
    config = Configurator()

    # Charger les routes
    from . import routes
    routes.include_routes(config)

    # Scanner les vues décorées
    config.scan('infra.pyramid_app.views')

    # Support TAL/METAL
    config.include('pyramid_chameleon')

    return config.make_wsgi_app()
