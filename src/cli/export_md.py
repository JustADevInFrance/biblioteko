import fitz  # PyMuPDF
import base64
import os
from mistralai import Mistral
from tempfile import TemporaryDirectory

# ---------------- CONFIG ----------------
API_KEY = os.getenv("a5s3EYGxxYPicvNfjbtntglitfSIelX7")  
INPUT_PDF = "input.pdf"
OUTPUT_MD = "output_final.md"
PAGES_PER_CHUNK = 5

# ---------------- CLIENT ----------------
client = Mistral(api_key=API_KEY)

# ---------------- UTILITAIRES ----------------

def split_pdf(input_pdf, pages_per_chunk, output_dir):
    """
    Découpe un PDF en sous-PDFs de N pages
    """
    doc = fitz.open(input_pdf)
    chunks = []

    for i in range(0, len(doc), pages_per_chunk):
        chunk_path = os.path.join(output_dir, f"chunk_{i//pages_per_chunk}.pdf")
        new_doc = fitz.open()

        for page_index in range(i, min(i + pages_per_chunk, len(doc))):
            new_doc.insert_pdf(doc, from_page=page_index, to_page=page_index)

        new_doc.save(chunk_path)
        chunks.append(chunk_path)

    return chunks


def pdf_to_base64(pdf_path):
    with open(pdf_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def ocr_and_correct_pdf(pdf_path):
    """
    OCR + correction du PDF (chunk)
    Retourne une liste de pages Markdown corrigées
    """
    pdf_base64 = pdf_to_base64(pdf_path)
    document_url = f"data:application/pdf;base64,{pdf_base64}"

    # --- OCR ---
    ocr_response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": document_url,
            "document_name": os.path.basename(pdf_path),
        },
    )

    corrected_pages = []

    # --- CORRECTION PAGE PAR PAGE ---
    for page_index, page in enumerate(ocr_response.pages):
        prompt = (
            "Corrige le texte extrait d’un scan OCR. "
            "Ne fais aucun commentaire, conserve uniquement le contenu. "
            "Respecte le Markdown.\n\n"
            + page.markdown
        )

        response = client.chat.complete(
            model="mistral-large-latest",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )

        corrected_pages.append(response.choices[0].message.content)

    return corrected_pages

# ---------------- PIPELINE PRINCIPAL ----------------

def process_pdf(input_pdf, output_md, pages_per_chunk):
    all_pages_md = []

    with TemporaryDirectory() as tmpdir:
        chunks = split_pdf(input_pdf, pages_per_chunk, tmpdir)

        for chunk_index, chunk_pdf in enumerate(chunks):
            print(f"📄 Traitement du chunk {chunk_index + 1}/{len(chunks)}")

            pages_md = ocr_and_correct_pdf(chunk_pdf)

            for i, page_md in enumerate(pages_md):
                global_page_number = chunk_index * pages_per_chunk + i + 1
                all_pages_md.append(f"## Page {global_page_number}\n\n{page_md}")

    # --- SAUVEGARDE FINALE ---
    with open(output_md, "w", encoding="utf-8") as f:
        f.write("\n\n".join(all_pages_md))

    print(f"\n🎉 Markdown final généré : {output_md}")

# ---------------- RUN ----------------

if __name__ == "__main__":
    if not API_KEY:
        raise RuntimeError("❌ MISTRAL_API_KEY manquante")

    process_pdf(INPUT_PDF, OUTPUT_MD, PAGES_PER_CHUNK)
