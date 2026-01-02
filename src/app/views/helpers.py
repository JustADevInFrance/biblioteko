def build_navbar(request):
    navbar_links = [
        ("Accueil", "/"),
        ("Oeuvres", "/oeuvres")
    ]

    if request.session.get("username"):
        navbar_links.append(("Proposer une oeuvre", "/upload"))
        navbar_links.append(("Demande de rôle", "/demande-role"))

        if request.session.get("role") == "bibliothecaire":
            navbar_links.append(("Gestion bibliothécaire", "/gestion_biblio"))

        navbar_links.append(("Se déconnecter", "/logout"))
    else:
        navbar_links.append(("Se connecter", "/connect"))

    return navbar_links
