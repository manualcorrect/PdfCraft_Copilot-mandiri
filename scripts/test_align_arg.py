import os
import sys

sys.path.insert(0, os.path.abspath('.'))
sys.stdout.reconfigure(encoding='utf-8')

from src.pdfcraft_client import PdfCraftClient
import pdfplumber

client = PdfCraftClient()
src_pdf = os.path.abspath('templates/master_page_1.pdf')
test_pdf = os.path.abspath('output/test_align_right.pdf')

doc_id = client.doc_open(src_pdf)

# P#46 rect=[393.72, 343.92, 432.0, 351.92]
# If we set align="right", what happens?
try:
    res1 = client.edit_text(doc_id, 1, paragraph=46, text="-500.000,00", align="right")
    print(f"Res1: {res1}")
except Exception as e:
    print(f"Error res1: {e}")

try:
    res2 = client.edit_text(doc_id, 1, paragraph=44, text="354.955,00", align="right")
    print(f"Res2: {res2}")
except Exception as e:
    print(f"Error res2: {e}")

client.doc_save(doc_id, test_pdf)
client.doc_close(doc_id)

with pdfplumber.open(test_pdf) as pdf:
    words = pdf.pages[0].extract_words()
    print("\nWith align='right':")
    for w in words:
        if any(k in w['text'] for k in ['354.955', '-500.000']):
            print(f"Word: {w['text']:15s} x0={w['x0']:6.2f} x1={w['x1']:6.2f} top={w['top']:6.2f}")
