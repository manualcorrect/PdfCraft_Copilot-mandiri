import sys, os
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\okt\0.pdf"

with PdfCraftClient() as client:
    doc_id = client.doc_open(pdf_path)
    for p_num in range(1, 8):
        paras = client.get_paragraphs(doc_id, page=p_num)
        print(f"\n--- Page {p_num} (total {len(paras)} paras) ---")
        for p in paras:
            if p['rect'][1] < 150:
                print(f"  para {p['paragraph']:2d} (rect={[round(x,1) for x in p['rect']]}): {p['text']!r}")
    client.doc_close(doc_id)
