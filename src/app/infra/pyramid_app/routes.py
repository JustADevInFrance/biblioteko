def include_routes(config):
    config.add_route("home", "/")
    config.add_route("upload", "/upload")
    config.add_route("moderation", "/moderation")
    config.add_route("fond_commun", "/fond_commun")
    
    config.add_route("moderation_view", "/moderation/view/{filename}")
    config.add_route("moderation_approve", "/moderation/approve/{filename}")
    config.add_route("moderation_reject", "/moderation/reject/{filename}")
    config.add_route("fond_commun_download", "/fond_commun/download/{filename}")
    config.add_route("fond_commun_view", "/fond_commun/view/{filename}")
