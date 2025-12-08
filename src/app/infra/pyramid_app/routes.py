def include_routes(config):
    """Définition des routes Pyramid."""
    config.add_route("home", "/")
    config.add_route("upload", "/upload")
    config.add_route("moderation", "/moderation")
    config.add_route("creation_de_compte", "/creation_de_compte")

