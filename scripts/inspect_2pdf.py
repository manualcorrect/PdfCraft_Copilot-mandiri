import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from pdfcraft_client import PdfCraftClient
import pdfplumber

pdf_source = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\2.pdf"

with pdfplumber.open(pdf_source) as pdf:
    for p_idx in range(len(pdf.pages)):
        page = pdf.pages[p_idx]
        words = [w for w in page.extract_words() if 40 <= w['x0'] <= 110 and w['top'] > (300 if p_idx==0 else 200)]
        print(f"=== Page {p_idx+1} Date/Time Words in 2.pdf ===")
        for w in words[:15]:
            print(f"  top={w['top']:.1f}, x0={w['x0']:.1f}, text={repr(w['text'])}")
