from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory

def main(global_config, **settings):
    """Fonction principale qui renvoie l'application WSGI Pyramid."""
    config = Configurator(settings=settings)
    
    # Activer Chameleon pour les templates .pt
    config.include('pyramid_chameleon')
    
    # Définir les routes
    config.add_route('home', '/')
    config.add_route('oeuvres', '/oeuvres')
    config.add_route('connect', '/connect')
    config.add_route('logout', '/logout')
    config.add_route('upload', '/upload')
    config.add_route('apercu_prop', '/proposition/{id}/apercu')
    config.add_route('gestion_biblio', '/gestion_biblio')
    config.add_route('apercu_oeuvre', '/oeuvre/{id}/apercu')
    
    # Scanner automatiquement toutes les vues dans le package views/
    config.scan('app.views')
    
    # Fichiers statiques (CSS, JS, images)
    config.add_static_view(name='static', path='app:static', cache_max_age=3600)

    session_factory = SignedCookieSessionFactory(
        "key"
    )

    config.set_session_factory(session_factory)
    
    return config.make_wsgi_app()
