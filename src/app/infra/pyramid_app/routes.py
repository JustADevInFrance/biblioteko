def include_routes(config):
    """Définition des routes Pyramid."""
    config.add_route("home", "/")
    config.add_route("upload", "/upload")
    config.add_route("moderation", "/moderation")
