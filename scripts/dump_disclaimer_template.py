import os
import sys

sys.path.insert(0, os.path.abspath('.'))
sys.stdout.reconfigure(encoding='utf-8')

from src.pdfcraft_client import PdfCraftClient

client = PdfCraftClient()
p_disc = os.path.abspath('templates/master_page_disclaimer_standalone.pdf')
doc_id = client.doc_open(p_disc)
paras = client.get_paragraphs(doc_id, 1)

print("=== master_page_disclaimer_standalone paragraphs ===")
for p in paras:
    rect = [round(x, 2) for x in p['rect']]
    print(f"P#{p['paragraph']:3d} | rect={rect} | text={repr(p['text'])}")

client.doc_close(doc_id)
