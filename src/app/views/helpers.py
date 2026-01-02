def build_navbar(request):
    navbar_links = [
        ("Accueil", "/"),
        ("Oeuvres", "/oeuvres")
    ]

    role = request.session.get("role")
    username = request.session.get("username")

    if username:
        navbar_links.append(("Proposer une oeuvre", "/upload"))

        if role == "membre":
            navbar_links.append(("Demande de rôle", "/demande-role"))

        if role == "bibliothecaire":
            navbar_links.append(("Gestion bibliothécaire", "/gestion_biblio"))

        if role == "admin":
            navbar_links.append(("Administration", "/admin/demandes"))

        navbar_links.append(("Se déconnecter", "/logout"))
    else:
        navbar_links.append(("Se connecter", "/connect"))

    return navbar_links


