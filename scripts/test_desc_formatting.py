import os
import sys

sys.path.insert(0, os.path.abspath('.'))
sys.stdout.reconfigure(encoding='utf-8')

from src.pdfcraft_client import PdfCraftClient
import pdfplumber

client = PdfCraftClient()
src_pdf = os.path.abspath('templates/master_page_1.pdf')
test_pdf = os.path.abspath('output/test_desc_layout.pdf')

doc_id = client.doc_open(src_pdf)

# P#55 is the description of row 3 (rect=[124.0, 430.92, 192.64, 448.92])
# Let's test with width=230.0
tx3_desc = "Transfer dari BANK MANDIRI\nSIGIT BUDHI ARYONO 1550009926679"
client.edit_text(doc_id, 1, paragraph=55, text=tx3_desc, width=230.0)

# P#61 is the description of row 4 (rect=[124.0, 471.92, 187.64, 499.92])
tx4_desc = "Penarikan tunai di ATM\nBANK MANDIRI SRG IM CIRUAS 01"
client.edit_text(doc_id, 1, paragraph=61, text=tx4_desc, width=230.0)

client.doc_save(doc_id, test_pdf)
client.doc_close(doc_id)

with pdfplumber.open(test_pdf) as pdf:
    print("=== Extracted Words for Row 3 & Row 4 ===")
    for w in pdf.pages[0].extract_words():
        if 420 <= w['top'] <= 500 and 120 <= w['x0'] <= 360:
            print(f"  {w['text']:25s} | x0={w['x0']:6.2f}, x1={w['x1']:6.2f}, top={w['top']:6.2f}, bottom={w['bottom']:6.2f}")
