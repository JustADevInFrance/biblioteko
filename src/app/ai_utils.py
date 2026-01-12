import os
import json
import tempfile
import base64
import io
import logging
import requests
from dotenv import load_dotenv
from pdf2image import convert_from_path
from PIL import Image

# =========================================================
# CONFIG
# =========================================================

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", ".env")
dotenv_path = os.path.abspath(dotenv_path)
load_dotenv(dotenv_path)

PIXTRAL_API_KEY = os.getenv("PIXTRAL_API_KEY")
if not PIXTRAL_API_KEY:
    raise RuntimeError("PIXTRAL_API_KEY manquant")

# API CHAT (OBLIGATOIRE pour Pixtral images)
CHAT_API_URL = "https://api.mistral.ai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {PIXTRAL_API_KEY}",
    "Content-Type": "application/json"
}

import os

# Si Windows, utiliser le chemin Windows, sinon Linux
if os.name == "nt":  # Windows
    POPPLER_PATH = r"C:\popper\Library\bin"
else: 
    POPPLER_PATH = "/usr/bin"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

MAX_IMAGE_SIZE = (2000, 2000)

# =========================================================
# OCR PIXTRAL (IMAGE → MARKDOWN)
# =========================================================

def analyze_with_pixtral_from_image(image: Image.Image) -> str:
    """
    Fait de l'OCR sur une image PIL et retourne le texte en Markdown via Pixtral.
    L'image est convertie en PNG et encodée en base64.
    """
    logger.info("OCR Pixtral image...")

    # Redimensionner pour limiter la taille
    image.thumbnail(MAX_IMAGE_SIZE, Image.Resampling.LANCZOS)

    # Sauvegarder en PNG dans un buffer mémoire
    buffer = io.BytesIO()
    image.save(buffer, format="PNG", optimize=True)
    image_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    payload = {
        "model": "mistral-small-latest",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}},
                    {"type": "text", "text": (
                        "Fais de l'OCR sur cette image et rends le texte en Markdown. "
                        "Respecte fidèlement la mise en page. "
                        "N'invente rien."
                    )}
                ]
            }
        ],
        "temperature": 0
    }

    response = requests.post(
        "https://api.mistral.ai/v1/chat/completions",
        headers=HEADERS,
        json=payload,
        timeout=120
    )

    if response.status_code != 200:
        logger.error(f"OCR FAILED {response.status_code}: {response.text[:500]}")
        raise RuntimeError("Erreur OCR Pixtral")

    result = response.json()
    return result["choices"][0]["message"]["content"].strip()



# =========================================================
# PDF SCANNÉ → MARKDOWN
# =========================================================

def pdf_scanned_to_markdown(pdf_path: str) -> str:
    """
    Convertit un PDF scanné en texte Markdown via OCR Pixtral.
    Chaque page est redimensionnée pour limiter la taille.
    """

    logger.info(f"Conversion PDF scanné: {pdf_path}")

    all_text = []
    page_number = 1

    while True:
        pages = convert_from_path(
            pdf_path,
            dpi=180,
            first_page=page_number,
            last_page=page_number,
            poppler_path=POPPLER_PATH
        )

        if not pages:
            break

        page = pages[0]
        logger.info(f"OCR page {page_number}")

        try:
            text = analyze_with_pixtral_from_image(page)
            logger.info(f"Page {page_number} OK")
            all_text.append(text)
        except Exception as e:
            logger.error(f"Erreur OCR page {page_number}: {e}")

        page_number += 1

    logger.info("Conversion PDF terminée")
    full_text = "\n\n".join(all_text)
    return refine_markdown(full_text)

def refine_markdown(md_text: str) -> str:
    prompt = (
        "Tu es un assistant qui renvoie STRICTEMENT du code Markdown.\n"
        "Ne rajoute aucun commentaire, aucune note, aucun texte explicatif.\n"
        "Corrige les répétitions, les titres multiples, "
        "réécris les paragraphes mal formés, "
        "mais conserve toutes les informations et images.\n"
        "Rends le résultat propre et lisible.\n\n"
        + md_text[:12000]  # limiter si nécessaire
    )

    payload = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
    }

    response = requests.post(CHAT_API_URL, headers=HEADERS, json=payload, timeout=180)
    result = response.json()
    return result["choices"][0]["message"]["content"].strip()

# =========================================================
# EXTRACTION MÉTADONNÉES
# =========================================================

def extract_metadata_from_text(text: str) -> dict:
    if not text.strip():
        return {}

    payload = {
        "model": "mistral-small-latest",
        "messages": [
            {
                "role": "user",
                "content": (
                    "Voici un texte extrait d'un livre.\n"
                    "Retourne STRICTEMENT un JSON avec :\n"
                    "{ \"titre\": str, \"auteur\": str, \"annee\": int|null, \"resume\": str }\n\n"
                    + text[:12000]
                )
            }
        ],
        "temperature": 0
    }

    response = requests.post(
        CHAT_API_URL,
        headers=HEADERS,
        json=payload,
        timeout=120
    )

    if response.status_code != 200:
        logger.error("Erreur extraction métadonnées")
        return {}

    try:
        return json.loads(response.json()["choices"][0]["message"]["content"])
    except Exception:
        return {}

# =========================================================
# CONTENU EXPLICITE / DROITS
# =========================================================

def ai_check_content(text: str) -> tuple[bool, bool]:
    if not text.strip():
        return False, True

    payload = {
        "model": "mistral-small-latest",
        "messages": [
            {
                "role": "user",
                "content": (
                    "Analyse le texte suivant et réponds STRICTEMENT en JSON :\n"
                    "{ \"est_explicite\": bool, \"libre_de_droit\": bool }\n\n"
                    + text[:8000]
                )
            }
        ],
        "temperature": 0
    }

    response = requests.post(
        CHAT_API_URL,
        headers=HEADERS,
        json=payload,
        timeout=120
    )

    if response.status_code != 200:
        logger.error("Erreur analyse contenu")
        return False, True

    try:
        data = json.loads(response.json()["choices"][0]["message"]["content"])
        return bool(data.get("est_explicite", False)), bool(data.get("libre_de_droit", True))
    except Exception:
        return False, True

# =========================================================
# API HAUT NIVEAU
# =========================================================

def pdf_to_markdown_with_metadata(pdf_path: str) -> tuple[str, dict]:
    markdown = pdf_scanned_to_markdown(pdf_path)
    metadata = extract_metadata_from_text(markdown)
    return markdown, metadata

def md_extract_metadata(md_path: str) -> tuple[str, dict]:
    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()
    metadata = extract_metadata_from_text(text)
    return text, metadata
