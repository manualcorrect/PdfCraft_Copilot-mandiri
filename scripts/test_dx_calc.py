import os
import sys

sys.path.insert(0, os.path.abspath('.'))
sys.stdout.reconfigure(encoding='utf-8')

from src.pdfcraft_client import PdfCraftClient
import pdfplumber

client = PdfCraftClient()
src_pdf = os.path.abspath('templates/master_page_1.pdf')
test_pdf = os.path.abspath('output/test_dx.pdf')

doc_id = client.doc_open(src_pdf)

# P#46 in template has rect=[393.72, 343.92, 432.0, 351.92] (text='-2.500,00')
# In previous run, new text '-500.000,00' had width = 49.84 pt.
# If start is 393.72, then end is 393.72 + 49.84 = 443.56.
# To make end = 432.00, we want dx = 432.00 - 443.56 = -11.56.
client.edit_text(doc_id, 1, paragraph=46, text="-500.000,00", dx=-11.56)

# P#44 in template has rect=[522.16, 343.92, 571.0, 351.92] (text='6.364.500,81')
# '354.955,00' had width = 43.68 pt.
# If start is 522.16, then end is 522.16 + 43.68 = 565.84.
# To make end = 571.00, we want dx = 571.00 - 565.84 = +5.16.
client.edit_text(doc_id, 1, paragraph=44, text="354.955,00", dx=5.16)

client.doc_save(doc_id, test_pdf)
client.doc_close(doc_id)

with pdfplumber.open(test_pdf) as pdf:
    words = pdf.pages[0].extract_words()
    print("\nWith DX shifts:")
    for w in words:
        if any(k in w['text'] for k in ['354.955', '-500.000']):
            print(f"Word: {w['text']:15s} x0={w['x0']:6.2f} x1={w['x1']:6.2f} top={w['top']:6.2f}")
