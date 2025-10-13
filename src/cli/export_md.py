"""
Pipeline PDF scanné -> Markdown via OCR + API IA (OpenAI)
- OCR Tesseract (multi-langues)
- Détection automatique de la langue
- IA pour corriger et structurer en Markdown
- Extraction de métadonnées 


import fitz
import pytesseract
import re
from langdetect import detect
from tqdm import tqdm
import json
import openai

# ----------------- OCR + Nettoyage -----------------

def ocr_page(page, langs="fra+eng+deu+dpa"):
    pix = page.get_pixmap(dpi=300)
    img_bytes = pix.tobytes("png")
    text = pytesseract.image_to_string(img_bytes, lang=langs)
    return clean_text(text)

def clean_text(text: str) -> str:
    lines = text.splitlines()
    cleaned = []
    for line in lines:
        if re.match(r'^\s*\d+\s*$', line):
            continue
        cleaned.append(line.strip())
    return "\n".join(l for l in cleaned if l)

# ----------------- Appel OpenAI API pour structuration -----------------

def ask_ai_remote(text, lang_code):
    prompt = f
    You are an assistant that processes OCR text in language '{lang_code}'.
    Task:
    - Correct OCR errors
    - Format text in Markdown (titles, paragraphs, lists)
    - Extract metadata if visible (author, publisher, year, copyright)
    - Keep original language
    - Output cleaned Markdown only
    OCR Text:
    {text}
    
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response['choices'][0]['message']['content']

# ----------------- Extraction de métadonnées basique -----------------

def extract_metadata(text):
    meta = {}
    if m := re.search(r'(?i)(par|by)\s+([A-Z][^\n]{2,50})', text):
        meta["author"] = m.group(2).strip()
    if y := re.search(r'(?<!\d)(19|20)\d{2}(?!\d)', text):
        meta["year"] = y.group(0)
    if c := re.search(r'(?i)(copyright|©).(0,80)', text):
        meta["copyright"] = c.group(0).strip()
    if p := re.search(r'(?i)(Éditions?|Publisher)[:\s]+([^\n]{3,60})', text):
        meta["publisher"] = p.group(2).strip()
    return meta

# ----------------- Pipeline principal -----------------

def process_pdf(pdf_path, output_md, langs="fra+eng+deu+spa", max_pages=None):
    doc = fitz.open(pdf_path)
    metadata_candidates = []

    with open(output_md, "w", encoding="utf-8") as out:
        for i, page in enumerate(tqdm(doc, desc="Processing pages")):
            if max_pages and i >= max_pages:
                break
            
            raw_text = ocr_page(page, langs=langs)
            if not raw_text.strip():
                continue

            try:
                lang_code = detect(raw_text)
            except:
                lang_code = "unknown"
            
            md_text = ask_ai_remote(raw_text, lang_code)
            out.write(f"\n\n## Page {i+1}\n\n{md_text}")

            if i < 5:
                metadata_candidates.append(md_text)

    joined = "\n".join(metadata_candidates)
    meta = extract_metadata(joined)
    with open(output_md.replace(".md", ".metadata.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    print(f"Markdown saved to {output_md}")
    print(f"Metadata saved to {output_md.replace('.md', '.metadata.json')}")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", help="Input scanned PDF")
    parser.add_argument("output", help="Output Markdown file")
    parser.add_argument("--langs", default="fra+eng+deu+spa", help="Tesseract OCR languages")
    parser.add_argument("--pages", type=int, default=None, help="Limit pages for testing")
    parser.add_argument("--api_key", required=True, help="OpenAI API key")
    args = parser.parse_args()

    openai.api_key = args.api_key
    process_pdf(args.pdf, args.output, langs=args.langs, max_pages=args.pages)
"""

import fitz
import io
import json
import re
import os
from PIL import Image
from tqdm import tqdm
from dotenv import load_dotenv
import requests

# Charger la clé API depuis .env
load_dotenv()
MISTRAL_API_KEY = os.getenv("PIXTRAL_API_KEY")

if not MISTRAL_API_KEY:
    raise RuntimeError("Clé API Mistral non trouvée dans le fichier .env")

# ----------------------------------- Fonction utilitaires ----------------------------------- 

def extract_image_from_page(page):
    """
    Rend une image PNG haute résolution depuis une page PDF.
    """
    pix = page.get_pixmap(dpi=300)
    return pix.tobytes("png")

def ask_pixtral_for_markdown(img_bytes):
    """
    Envoie une image à l'API Pixtral pour OCR + structuration Markdown
    """
    response = requests.post(
        "https://api.mistral.ai/v1/chat/completions",
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json",
        },
        json = {
            "model": "pixtral-12b-2409",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": (
                            "Extract all readable text from the following scanned book page, "
                            "correct OCR errors, preserve the original language, and format it as Markdown. "
                            " Include metadata if visible (author, publisher, year copyright)."
                        )},
                        {"type": "image_url", "image_url": "data:image/png;base64," + img_bytes.decode("latin1")}
                    ],
                }
            ],
        },
    )

    if response.status_code != 200:
        raise RuntimeError(f"Pixtral API error: {response.text}")
    
    data = response.json()
    return data["choices"][0]["message"]["content"]

def extract_metadata(text):
    meta = {}
    if m := re.search(r'(?i)(par|by)\s+([A-Z][^\n]{2-50})', text):
        meta["author"] = m.group(2).strip()
    if y := re.search(r'(?<!\d)(19|20)\d{2}(?!\d)', text):
        meta["year"] = y.group(0)
    if c := re.search(r'(?i)(copyright|©).{0,80}', text):
        meta["copyright"] = c.group(0).strip()
    if p := re.search(r'(?i)(Editions?|Publisher)[:\s]+([^\n]{3,60})', text):
        meta["publisher"] = p.group(2).strip()
    return meta

# ----------------------------------- Pipeline principal -----------------------------------

def process_pdf(pdf_path, output_md, max_pages=None):
    import base64

    doc = fitz.open(pdf_path)
    metadata_candidates = []

    with open(output_md, "w", encoding="utf-8") as out:
        for i, page in enumerate(tqdm(doc, desc="Processing pages")):
            if max_pages and i >= max_pages:
                break
            
            try:
                img_bytes = extract_image_from_page(page)
                img_base64 = base64.b64encode(img_bytes)
                md_text = ask_pixtral_for_markdown(img_base64)
            except Exception as e:
                print(f"Error processing page {i+1}: {e}")
                continue
            
            out.write(f"\n\n##Page {i+1}\n\n{md_text}")

            if i < 5:
                metadata_candidates.append(md_text)
    
    joined = "\n".join(metadata_candidates)
    meta = extract_metadata(joined)
    with open(output_md.replace(".md", ".metadata.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    
    print(f"Markdown saved to {output_md}")
    print(f"Metadata saved to {output_md.replace('.md', '.metadata.json')}")

# ----------------------------------- CLI -----------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", help="Input scanned PDF")
    parser.add_argument("output", help="Output Markdown file")
    parser.add_argument("--pages", type=int, default=None, help="Limit pages for testing")
    args = parser.parse_args()

    process_pdf(args.pdf, args.output, max_pages=args.pages)