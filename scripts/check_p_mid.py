import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from pdfcraft_client import PdfCraftClient

with PdfCraftClient() as client:
    doc_id = client.doc_open('templates/master_page_intermediate.pdf')
    paras = client.get_paragraphs(doc_id, page=1)
    for p in paras:
        if abs(p['rect'][1] - 733.92) < 25:
            print(f"P{p['paragraph']}: y0={p['rect'][1]:.2f}, x0={p['rect'][0]:.2f}, text={repr(p['text'])}")
    client.doc_close(doc_id)
