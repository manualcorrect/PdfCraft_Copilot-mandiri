import sys
sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient

pdf_src = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\aug\0.pdf"

with PdfCraftClient() as client:
    doc_id = client.doc_open(pdf_src)
    for p_num in [2, 3]:
        paras = client.get_paragraphs(doc_id, page=p_num)
        print(f"\n--- Page {p_num} Headers ---")
        for p in paras:
            if p["rect"][1] < 140 and any(k in p["text"] for k in ["Jun", "Sep", "ROY", "Aries"]):
                print(f"Para {p['paragraph']:2d}: text='{p['text']}' rect={p['rect']}")
    client.doc_close(doc_id)
