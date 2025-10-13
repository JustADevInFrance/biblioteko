import base64
from mistralai import Mistral
import os

# --- CONFIGURATION ---
api_key = "0gGtjfCDKLiiaZzMdNzTx9PFiB7Q0P8D"  # ta clé API
pdf_path = "extrait_p5_p6.pdf"
output_md = "output_corrected.md"

# --- INITIALISATION CLIENT ---
client = Mistral(api_key=api_key)

# --- LECTURE ET ENCODAGE PDF EN BASE64 ---
with open(pdf_path, "rb") as f:
    pdf_base64 = base64.b64encode(f.read()).decode("utf-8")

document_url = f"data:application/pdf;base64,{pdf_base64}"

# --- OCR DU DOCUMENT ---
ocr_response = client.ocr.process(
    model="mistral-ocr-latest",
    document={
        "type": "document_url",
        "document_url": document_url,
        "document_name": pdf_path
    },
    include_image_base64=False
)

# --- CORRECTION PAGE PAR PAGE ---
corrected_pages = []

for i, page in enumerate(ocr_response.pages):
    raw_md = page.markdown

    # Prompt pour correction
    prompt = (
    "corrige le texte extrait d’un scan OCR. sans mettre des commentaires que le contenu: \n"
    + raw_md
)


    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[{"role": "user", "content": prompt}],
    )

    # Récupération du texte corrigé
    corrected_md = response.choices[0].message.content
    corrected_pages.append(corrected_md)

    print(f" Page {i+1} corrigée")

# --- FUSION ET SAUVEGARDE ---
full_md = "\n\n".join(corrected_pages)

with open(output_md, "w", encoding="utf-8") as f:
    f.write(full_md)

print(f"\n🎉 OCR + correction terminés ! Markdown corrigé enregistré dans {output_md}")

