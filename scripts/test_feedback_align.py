import os
import sys

sys.path.insert(0, os.path.abspath('.'))
sys.stdout.reconfigure(encoding='utf-8')

from src.pdfcraft_client import PdfCraftClient
import pdfplumber

client = PdfCraftClient()
src_pdf = os.path.abspath('templates/master_page_1.pdf')
test_pdf = os.path.abspath('output/test_feedback_align.pdf')

doc_id = client.doc_open(src_pdf)

# Test 1: P#46 (Nominal, target X1 = 432.00)
# Step 1: Update text
client.edit_text(doc_id, 1, paragraph=46, text="-500.000,00")

# Step 2: Read actual paragraph rect
paras = client.get_paragraphs(doc_id, 1)
p46 = next(p for p in paras if p['paragraph'] == 46)
curr_x1 = p46['rect'][2]
dx = 432.00 - curr_x1
print(f"P#46 after text edit: rect={p46['rect']}, curr_x1={curr_x1}, needed dx={dx:.4f}")

# Step 3: Shift by dx
client.edit_text(doc_id, 1, paragraph=46, dx=dx)

# Test 2: P#44 (Saldo, target X1 = 571.00)
client.edit_text(doc_id, 1, paragraph=44, text="354.955,00")
paras = client.get_paragraphs(doc_id, 1)
p44 = next(p for p in paras if p['paragraph'] == 44)
curr_x1_saldo = p44['rect'][2]
dx_saldo = 571.00 - curr_x1_saldo
print(f"P#44 after text edit: rect={p44['rect']}, curr_x1={curr_x1_saldo}, needed dx={dx_saldo:.4f}")
client.edit_text(doc_id, 1, paragraph=44, dx=dx_saldo)

client.doc_save(doc_id, test_pdf)
client.doc_close(doc_id)

with pdfplumber.open(test_pdf) as pdf:
    words = pdf.pages[0].extract_words()
    print("\nVerification in saved PDF:")
    for w in words:
        if any(k in w['text'] for k in ['354.955', '-500.000']):
            print(f"Word: {w['text']:15s} x0={w['x0']:6.2f} x1={w['x1']:6.2f} top={w['top']:6.2f}")
