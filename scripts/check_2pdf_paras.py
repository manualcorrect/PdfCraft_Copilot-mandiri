import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from pdfcraft_client import PdfCraftClient

pdf_source = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\2.pdf"

with PdfCraftClient() as client:
    doc_id = client.doc_open(pdf_source)
    for p_num in range(1, 5):
        paras = client.get_paragraphs(doc_id, page=p_num)
        print(f"\n==================== 2.pdf PAGE {p_num} (Total paras: {len(paras)}) ====================")
        min_top = 300 if p_num == 1 else 180
        for p in paras:
            if p['rect'][1] >= min_top:
                print(f"  P{p['paragraph']:02d}: y0={p['rect'][1]:.1f}, x0={p['rect'][0]:.1f}, text={repr(p['text'])[:60]}")
    client.doc_close(doc_id)
