import sys
sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient
import pdfplumber

sep_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_SEP_2026.pdf"

print("--- Checking REK_GALANG_SEP_2026.pdf structure ---")
with pdfplumber.open(sep_path) as pdf:
    for page_idx, page in enumerate(pdf.pages, 1):
        words = page.extract_words()
        no_words = [w for w in words if abs(w['x0'] - 20.0) < 5 and 200 < w['top'] < 780 and w['text'].isdigit()]
        print(f"Page {page_idx}: found {len(no_words)} row numbers: {[w['text'] for w in no_words]}")
