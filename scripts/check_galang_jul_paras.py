import sys
import os
sys.path.append(os.path.abspath("src"))
sys.stdout.reconfigure(encoding='utf-8')
from pdfcraft_client import PdfCraftClient

galang_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\REK GALANG JUL 2026.pdf"

with PdfCraftClient() as client:
    doc_id = client.doc_open(galang_path)
    print("Paragraphs in authentic REK GALANG JUL 2026.pdf:")
    for p in client.get_paragraphs(doc_id, page=1):
        if p["rect"][1] < 160:
            print(f"P#{p['paragraph']:2d} rect={p['rect']} text={repr(p['text'])}")
    client.doc_close(doc_id, discard_changes=True)
