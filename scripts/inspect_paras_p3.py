import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

with PdfCraftClient() as client:
    doc_id = client.doc_open(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\aug\0.pdf')
    paras = client.get_paragraphs(doc_id, page=3)
    for p in paras:
        if p['rect'][1] > 200:
            print(f"Para {p['paragraph']:2d} [rect={p['rect']}]: {repr(p['text'])}")
    client.doc_close(doc_id)
