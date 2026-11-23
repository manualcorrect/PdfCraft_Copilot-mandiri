import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient
import pdfplumber

client = PdfCraftClient()
doc_id = client.doc_open(r"scratch/test_sal_para.pdf")

client.edit_text(doc_id, page=3, paragraph=81, text='34 7.815.988,81')
client.doc_save(doc_id)
client.doc_close(doc_id)

with pdfplumber.open(r"scratch/test_sal_para.pdf") as pdf:
    p3 = pdf.pages[2]
    words = p3.extract_words()
    for w in sorted([w for w in words if 728 <= w['top'] <= 745], key=lambda x: x['x0']):
        print(f"'{w['text']}' at x0={w['x0']:.2f}, x1={w['x1']:.2f}")
