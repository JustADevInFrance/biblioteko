import fitz
import base64
import os
from tempfile import TemporaryDirectory
from mistralai import Mistral

# Client Mistral (clé via env)
client = Mistral(api_key="a5s3EYGxxYPicvNfjbtntglitfSIelX7")

# ---------------- FONCTION PRINCIPALE ----------------

def pdf_to_markdown(pdf_path: str, nombre_de_page: int = 10) -> str:
    """
    - prend un PDF en entrée
    - le découpe en sous-PDFs de `nombre_de_page`
    - envoie chaque sous-PDF au pipeline OCR + correction
    - fusionne tout dans un seul fichier Markdown
    """
    if not pdf_path.lower().endswith(".pdf"):
        raise ValueError("Entrée invalide : PDF attendu")

    output_md = os.path.splitext(pdf_path)[0] + ".md"
    pages_markdown = []

    with TemporaryDirectory() as tmpdir:
        # 1️⃣ Découpage du PDF
        doc = fitz.open(pdf_path)

        for start in range(0, len(doc), nombre_de_page):
            chunk_pdf = os.path.join(tmpdir, f"chunk_{start}.pdf")
            chunk = fitz.open()

            for p in range(start, min(start + nombre_de_page, len(doc))):
                chunk.insert_pdf(doc, from_page=p, to_page=p)

            chunk.save(chunk_pdf)

            # 2️⃣ Envoi du chunk au programme précédent (OCR Mistral)
            with open(chunk_pdf, "rb") as f:
                pdf_b64 = base64.b64encode(f.read()).decode("utf-8")

            ocr = client.ocr.process(
                model="mistral-ocr-latest",
                document={
                    "type": "document_url",
                    "document_url": f"data:application/pdf;base64,{pdf_b64}",
                    "document_name": os.path.basename(chunk_pdf),
                },
            )

            # 3️⃣ Correction page par page
            for page_index, page in enumerate(ocr.pages):
                prompt = (
                    "Corrige le texte extrait d’un scan OCR. "
                    "Ne fais aucun commentaire. "
                    "Respecte strictement le Markdown.\n\n"
                    + page.markdown
                )

                response = client.chat.complete(
                    model="mistral-large-latest",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0,
                )

                page_number = start + page_index + 1
                pages_markdown.append(
                    f"## Page {page_number}\n\n"
                    + response.choices[0].message.content
                )

    # 4️⃣ Fusion finale
    with open(output_md, "w", encoding="utf-8") as f:
        f.write("\n\n".join(pages_markdown))

    return output_md
