from datetime import datetime
from ..models import Oeuvre, Proposition, Session

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
