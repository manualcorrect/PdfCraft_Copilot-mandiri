import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from pdfcraft_client import PdfCraftClient

with PdfCraftClient() as client:
    for t_name in ['master_page_1.pdf', 'master_page_intermediate.pdf', 'master_page_disclaimer_inline.pdf']:
        path = os.path.join('templates', t_name)
        doc_id = client.doc_open(path)
        paras = client.get_paragraphs(doc_id, page=1)
        print(f"=== {t_name} Header Paras ===")
        for p in paras:
            if p['rect'][1] < 150 and p['rect'][0] < 300:
                print(f"P{p['paragraph']}: y0={p['rect'][1]:.2f}, x0={p['rect'][0]:.2f}, text={repr(p['text'])}")
        client.doc_close(doc_id)
