import sys
sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient

pdf_src = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\aug\0.pdf"

with PdfCraftClient() as client:
    doc_id = client.doc_open(pdf_src)
    paras = client.get_paragraphs(doc_id, page=1)
    for p in paras:
        if 330 <= p["rect"][1] <= 400:
            print(f"P1 Para {p['paragraph']:2d}: text='{p['text']}' rect={p['rect']}")
    client.doc_close(doc_id)
