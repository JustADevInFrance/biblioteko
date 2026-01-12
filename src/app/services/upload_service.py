import os
import tempfile
import logging

from ..models import Proposition
from ..ai_utils import *

logger = logging.getLogger(__name__)


def handle_upload(fichier, user_id, session):
    if fichier is None or not fichier.filename:
        raise ValueError("Aucun fichier envoyé")

    filename = fichier.filename.lower()
    suffix = os.path.splitext(filename)[1]
    file_data = fichier.file.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(file_data)
        temp_path = tmp.name

    try:
        if filename.endswith(".pdf"):
            contenu_markdown, meta_info = pdf_to_markdown_with_metadata(temp_path)
        elif filename.endswith(".md"):
            contenu_markdown, meta_info = md_extract_metadata(temp_path)
        else:
            raise ValueError("Format de fichier non supporté")

        # Vérification IA
        if contenu_markdown.strip():
            try:
                est_explicite, libre_de_droit = ai_check_content(contenu_markdown)
            except Exception as e:
                logger.error(f"Vérification IA impossible: {e}")
                est_explicite, libre_de_droit = False, True
        else:
            est_explicite, libre_de_droit = False, True

        prop = Proposition(
            titre=meta_info.get("titre", "Titre Inconnu"),
            auteur=meta_info.get("auteur", "Inconnu"),
            format_oeuvre="pdf" if filename.endswith(".pdf") else "md",
            contenu_markdown=contenu_markdown,
            est_explicite=est_explicite,
            libre_de_droit=libre_de_droit
        )
        prop.meta_info = str(meta_info)
        prop.utilisateur_id = user_id

        session.add(prop)
        session.commit()
        return prop

    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
