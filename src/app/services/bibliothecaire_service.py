from ..models import Oeuvre


def traiter_proposition(session, proposition, action):
    if action == "valider":
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
        session.delete(proposition)

    elif action == "rejeter":
        session.delete(proposition)

    session.commit()
