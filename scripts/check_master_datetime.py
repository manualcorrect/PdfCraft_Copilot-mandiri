import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from pdfcraft_client import PdfCraftClient

with PdfCraftClient() as client:
    doc_id = client.doc_open('templates/master_page_1.pdf')
    paras = client.get_paragraphs(doc_id, page=1)
    for p in paras:
        if 40 <= p['rect'][0] <= 85 and p['rect'][1] > 320:
            print(f"P{p['paragraph']}: y0={p['rect'][1]:.2f}, text={repr(p['text'])}")
    client.doc_close(doc_id)
