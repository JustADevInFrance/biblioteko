def home_content():
    return """
    <div class="p-5 mb-4 bg-light rounded-3">
      <div class="container-fluid py-5">
        <h1 class="display-5 fw-bold">Bienvenue dans Ma Bibliothèque !</h1>
        <p class="col-md-8 fs-4">Profitez de notre catalogue et ajoutez des oeuvres.</p>
        <a class="btn btn-primary btn-lg" href="/oeuvres" role="button">Voir les oeuvres</a>
      </div>
    </div>
    """

def build_navbar(request):
    links = [
        ("Accueil", "/"),
        ("Oeuvres", "/oeuvres")
    ]
    if request.session.get("username"):
        links.append(("Proposer une oeuvre", "/upload"))
        links.append(("Demande de rôle", "/demande-role"))
        if request.session.get("role") == "bibliothecaire":
            links.append(("Gestion bibliothécaire", "/gestion_biblio"))
        links.append(("Se déconnecter", "/logout"))
    else:
        links.append(("Se connecter", "/connect"))
    return links


def oeuvres_content(oeuvres, request):
    html = "<h2>Liste des Oeuvres</h2><ul class='list-group'>"

    for o in oeuvres:
        html += f"""
        <li class='list-group-item'>
            {o.titre} - {o.auteur} ({o.annee})
            <a class="btn btn-info"
               href="{request.route_url('apercu_oeuvre', id=o.id)}">
               Aperçu
            </a>
        </li>
        """

    html += "</ul>"
    return html


def connexion_form(message):
    return f"""
    <div class="d-flex justify-content-center mt-5">
      <div class="card shadow-sm" style="width: 400px;">
        <div class="card-body">
          <h2 class="card-title text-center mb-4">Connexion</h2>
          <div class="text-danger text-center mb-2">{message}</div>
          <form method="POST">
            <div class="mb-3">
              <label class="form-label">Nom d'utilisateur</label>
              <input type="text" class="form-control" name="username" required>
            </div>
            <div class="mb-3">
              <label class="form-label">Mot de passe</label>
              <input type="password" class="form-control" name="password" required>
            </div>
            <button type="submit" class="btn btn-primary w-100">Connexion</button>
          </form>
          <p class="text-center mt-3">
            Pas de compte ?
            <a href="/connect?form=inscription">S'inscrire</a>
          </p>
        </div>
      </div>
    </div>
    """

def inscription_form(message):
    return f"""
    <div class="d-flex justify-content-center mt-5">
      <div class="card shadow-sm" style="width: 400px;">
        <div class="card-body">
          <h2 class="card-title text-center mb-4">Inscription</h2>
          <div class="text-danger mb-2">{message}</div>
          <form method="POST">
            <div class="mb-3">
              <label class="form-label">Nom d'utilisateur</label>
              <input type="text" class="form-control" name="new_username" required>
            </div>
            <div class="mb-3">
              <label class="form-label">E-mail</label>
              <input type="email" class="form-control" name="new_email" required>
            </div>
            <div class="mb-3">
              <label class="form-label">Mot de passe</label>
              <input type="password" class="form-control" name="new_password" required>
            </div>
            <button type="submit" class="btn btn-success w-100">Créer le compte</button>
          </form>
          <p class="text-center mt-3">
            Déjà inscrit ?
            <a href="/connect?form=connexion">Se connecter</a>
          </p>
        </div>
      </div>
    </div>
    """



def upload_form(message):
    return f"""
    <div class="d-flex justify-content-center mt-5">
      <div class="card shadow-sm" style="width: 400px;">
        <div class="card-body">
          <h2 class="card-title text-center mb-4">Upload</h2>
          <div class="text-danger mb-2">{message}</div>
          <form method="POST" enctype="multipart/form-data">
            <div class="mb-3">
              <label class="form-label">Fichier PDF ou Markdown</label>
              <input type="file" name="fichier" accept=".pdf,.md" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-primary">Proposer l'oeuvre</button>
          </form>
        </div>
      </div>
    </div>
    """


def upload_form(message):
    return f"""
    <div class="d-flex justify-content-center mt-5">
      <div class="card shadow-sm" style="width: 400px;">
        <div class="card-body">
          <h2 class="card-title text-center mb-4">Upload</h2>
          <div class="text-danger mb-2">{message}</div>
          <form method="POST" enctype="multipart/form-data">
            <div class="mb-3">
              <label class="form-label">Fichier PDF ou Markdown</label>
              <input type="file" name="fichier" accept=".pdf,.md" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-primary">Proposer l'oeuvre</button>
          </form>
        </div>
      </div>
    </div>
    """

def apercu_oeuvre_content(oeuvre, html_content):
    return f"""
    <div class="container mt-4">
      <h2>{oeuvre.titre}</h2>
      <p><strong>Auteur:</strong> {oeuvre.auteur}</p>
      <p><strong>Format:</strong> {oeuvre.format_oeuvre}</p>
      <hr/>
      <div class="markdown-preview">
        {html_content}
      </div>
    </div>
    """


def gestion_biblio_content(propositions, request):
    html = ""
    for prop in propositions:
        html += f"""
        <div class="card mb-3">
            <div class="card-body">
                <h5 class="card-title">{prop.titre}</h5>
                <p><strong>Auteur:</strong> {prop.auteur}</p>
                <p><strong>Format:</strong> {prop.format_oeuvre}</p>
                <a class="btn btn-info"
                   href="{request.route_url('apercu_prop', id=prop.id)}">
                   Aperçu
                </a>
                <form method="post" style="display:inline;">
                    <input type="hidden" name="prop_id" value="{prop.id}">
                    <button class="btn btn-success" name="action" value="valider">
                        Valider
                    </button>
                    <button class="btn btn-danger" name="action" value="rejeter">
                        Rejeter
                    </button>
                </form>
            </div>
        </div>
        """
    return html

def demande_role_content(message):
    return f"""
    <h2>Demande de rôle bibliothécaire</h2>
    <p>Ce rôle permet de modérer et valider les oeuvres.</p>

    <div class="text-info">{message}</div>

    <form method="post">
        <button class="btn btn-warning">Demander le rôle</button>
    </form>
    """


def admin_demandes_content(demandes, request):
    rows = ""
    for d in demandes:
        rows += f"""
        <tr>
            <td>{d.utilisateur.username}</td>
            <td>{d.date_demande}</td>
            <td>
                <a class="btn btn-success"
                   href="{request.route_url('admin_accepter', id=d.id)}">
                   Accepter
                </a>
                <a class="btn btn-danger"
                   href="{request.route_url('admin_refuser', id=d.id)}">
                   Refuser
                </a>
            </td>
        </tr>
        """

    return f"""
    <h2>Demandes de rôle</h2>
    <table class="table">
        <tr>
            <th>Utilisateur</th>
            <th>Date</th>
            <th>Action</th>
        </tr>
        {rows}
    </table>
    """

