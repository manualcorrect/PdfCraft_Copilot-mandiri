import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

with PdfCraftClient() as client:
    doc_id = client.doc_open(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\sep\0.pdf')
    paras = client.get_paragraphs(doc_id, page=1)
    for p in paras:
        if "1650003584860" in p['text']:
            print(f"Para {p['paragraph']} [rect={p['rect']}]: {repr(p['text'])}")
    client.doc_close(doc_id)
