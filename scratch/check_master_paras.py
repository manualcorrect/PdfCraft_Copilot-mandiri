import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

with PdfCraftClient() as client:
    doc_id = client.doc_open('templates/master_page_1.pdf')
    paras = client.get_paragraphs(doc_id, page=1)
    for p in sorted(paras, key=lambda x: (x['rect'][1], x['rect'][0])):
        if p['rect'][1] > 250:
            print(f"P{p['paragraph']:2d}: rect={p['rect']}, text={repr(p['text'])}")
    client.doc_close(doc_id)
