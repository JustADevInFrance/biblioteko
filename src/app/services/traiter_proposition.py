from datetime import datetime
from pyramid.httpexceptions import HTTPFound
from ..models import Session, Oeuvre, Proposition

# --- TRAITEMENT DES PROPOSITIONS ---
def traiter_proposition(session, proposition, action):
    """
    Traite une proposition de bibliothécaire : validation ou rejet.
    Si validée, crée une Oeuvre à partir de la proposition.
    """
    if action == "valider":
        # Créer l'Oeuvre
        oeuvre = Oeuvre(
            titre=proposition.titre,
            auteur=proposition.auteur,
            annee=proposition.meta.get("annee") if proposition.meta else None,
            contenu_markdown=proposition.contenu_markdown,
            format_oeuvre=proposition.format_oeuvre,
            est_explicite=proposition.est_explicite,
            libre_de_droit=proposition.libre_de_droit,
            utilisateur_id=proposition.utilisateur_id,
            date_creation=proposition.date_creation
        )
        session.add(oeuvre)
        session.delete(proposition)  # Supprime la proposition après validation
        session.commit()
    elif action == "rejeter":
        session.delete(proposition)
        session.commit()


# --- HTML DES PROPOSITIONS ---
def gestion_biblio_content(propositions, request):
    html = ""
    for prop in propositions:
        html += f"""
        <div class="card mb-3">
            <div class="card-body">
                <h5 class="card-title">{prop.titre}</h5>
                <p class="card-text"><strong>Auteur:</strong> {prop.auteur}</p>
                <p class="card-text"><strong>Format:</strong> {prop.format_oeuvre}</p>
                <a class="btn btn-info" href="{request.route_url('apercu_prop', id=prop.id)}">Aperçu</a>
                <form method="post" style="display:inline;">
                    <input type="hidden" name="prop_id" value="{prop.id}">
                    <button type="submit" name="action" value="valider" class="btn btn-success">Valider</button>
                    <button type="submit" name="action" value="rejeter" class="btn btn-danger">Rejeter</button>
                </form>
            </div>
        </div>
        """
    if not html:
        html = "<p>Aucune proposition en attente.</p>"
    return html
