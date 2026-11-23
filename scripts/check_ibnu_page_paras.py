import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

pdf_src = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\0.pdf"

with PdfCraftClient() as client:
    doc_id = client.doc_open(pdf_src)
    for p_num in range(1, 8):
        paras = client.get_paragraphs(doc_id, page=p_num)
        p_pgs = [p for p in paras if p["rect"][1] < 130 and p["rect"][0] > 450]
        print(f"\n--- Page {p_num} ---")
        for p in p_pgs:
            print(f"Para {p['paragraph']}: rect={p['rect']} text='{p['text']}'")
    client.doc_close(doc_id)
