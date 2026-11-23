import os
import sys

sys.path.insert(0, os.path.abspath('.'))
sys.stdout.reconfigure(encoding='utf-8')

from src.pdfcraft_client import PdfCraftClient
import pdfplumber

client = PdfCraftClient()
src_pdf = os.path.abspath('templates/master_page_1.pdf')
test_pdf = os.path.abspath('output/test_split_name.pdf')

doc_id = client.doc_open(src_pdf)

# P#21 in master_page_1 is the name
client.edit_text(doc_id, 1, paragraph=21, text="GALANG PUTRA\nKURNIAWAN")

client.doc_save(doc_id, test_pdf)
client.doc_close(doc_id)

with pdfplumber.open(test_pdf) as pdf:
    print("=== Extracted Name Words ===")
    for w in pdf.pages[0].extract_words():
        if w['top'] < 130 and any(k in w['text'] for k in ['GALANG', 'PUTRA', 'KURNIAWAN']):
            print(f"  {w['text']:15s} | x0={w['x0']:6.2f}, x1={w['x1']:6.2f}, top={w['top']:6.2f}, bottom={w['bottom']:6.2f}")
