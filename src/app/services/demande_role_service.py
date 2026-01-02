from datetime import datetime
from ..models import DemandeRole


def demande_en_cours(session, user_id):
    return session.query(DemandeRole).filter_by(
        utilisateur_id=user_id,
        statut="en_attente"
    ).first()


def creer_demande(session, user_id):
    demande = DemandeRole(utilisateur_id=user_id)
    session.add(demande)
    session.commit()


def accepter_demande(session, demande):
    demande.statut = "accepte"
    demande.utilisateur.role = "bibliothecaire"
    demande.date_traitement = datetime.utcnow()
    session.commit()
