import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

with PdfCraftClient() as client:
    doc_id = client.doc_open(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\sep\0.pdf')
    for p_num in range(1, 5):
        print(f"=== PAGE {p_num} ===")
        paras = client.get_paragraphs(doc_id, page=p_num)
        for p in paras:
            if p['rect'][1] < 160:
                print(f"Para {p['paragraph']:2d} [rect={p['rect']}]: {repr(p['text'])}")
    client.doc_close(doc_id)
