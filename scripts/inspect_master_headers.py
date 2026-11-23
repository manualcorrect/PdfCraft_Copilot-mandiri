import os
import sys

sys.path.insert(0, os.path.abspath('.'))
sys.stdout.reconfigure(encoding='utf-8')

from src.pdfcraft_client import PdfCraftClient

client = PdfCraftClient()
p1 = os.path.abspath('templates/master_page_1.pdf')
doc_id = client.doc_open(p1)
paras = client.get_paragraphs(doc_id, 1)
print("=== master_page_1 paragraphs ===")
for i, p in enumerate(paras[:45]):
    rect = [round(x, 1) for x in p['rect']]
    print(f"P#{i:2d} | rect={rect} | text={repr(p['text'])}")
client.doc_close(doc_id)

p2 = os.path.abspath('templates/master_page_intermediate.pdf')
doc_id2 = client.doc_open(p2)
paras2 = client.get_paragraphs(doc_id2, 1)
print("\n=== master_page_intermediate paragraphs ===")
for i, p in enumerate(paras2[:25]):
    rect = [round(x, 1) for x in p['rect']]
    print(f"P#{i:2d} | rect={rect} | text={repr(p['text'])}")
client.doc_close(doc_id2)
