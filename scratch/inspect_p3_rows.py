import sys
sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient

pdf_src = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\aug\0.pdf"

with PdfCraftClient() as client:
    doc_id = client.doc_open(pdf_src)
    paras = client.get_paragraphs(doc_id, page=3)
    for p in paras:
        if 650 <= p["rect"][1] <= 760:
            print(f"Para {p['paragraph']:2d}: text='{p['text']}' rect={p['rect']}")
    client.doc_close(doc_id)
