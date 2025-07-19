# utils/rag_ocr_ingest.py

import os
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from datetime import datetime

# ✅ Explicitly set path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

SOURCE_DIR = "data/manual_feed"
OUTPUT_FILE = "data/knowledge/raw_extracted_text.txt"
os.makedirs("data/knowledge", exist_ok=True)


def extract_text_from_pdf(path):
    doc = fitz.open(path)
    all_text = []
    for page in doc:
        text = page.get_text()
        if text.strip():
            all_text.append(text)
        else:
            # fallback: render as image and use OCR
            pix = page.get_pixmap(dpi=300)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            ocr_text = pytesseract.image_to_string(img)
            all_text.append(ocr_text)
    return "\n".join(all_text)


def run_ocr_ingestion():
    files = [f for f in os.listdir(SOURCE_DIR) if f.lower().endswith(".pdf")]
    corpus = []
    for f in files:
        try:
            path = os.path.join(SOURCE_DIR, f)
            text = extract_text_from_pdf(path)
            corpus.append(f"# {f}\n{text}\n")
        except Exception as e:
            print(f"Error reading {f}: {e}")

    if corpus:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
            out.write("\n\n".join(corpus))
        print(f"✅ OCR output written to {OUTPUT_FILE}")
    else:
        print("⚠️ No text extracted.")


if __name__ == "__main__":
    run_ocr_ingestion()
