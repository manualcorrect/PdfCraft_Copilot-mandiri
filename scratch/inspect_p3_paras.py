import sys
sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient

pdf_src = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\aug\0.pdf"

with PdfCraftClient() as client:
    doc_id = client.doc_open(pdf_src)
    paras = client.get_paragraphs(doc_id, page=3)
    print(f"Total paragraphs on Page 3: {len(paras)}")
    for p in paras:
        txt = p["text"]
        rect = p["rect"]
        # Print if related to Tx 24 (UPAH, KARINA, 4.286) or Tx 33, 34
        if any(k in txt for k in ["KARINA", "UPAH", "4.286", "2452998221", "450.000", "1.000,00", "1.405", "1.855"]):
            print(f"Para {p['paragraph']:2d}: text='{txt}' rect={rect}")
    client.doc_close(doc_id)
