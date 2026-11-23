import sys
import os
sys.path.append(os.path.abspath("src"))
sys.stdout.reconfigure(encoding='utf-8')
from pdfcraft_client import PdfCraftClient

with PdfCraftClient() as client:
    doc_id = client.doc_open(r"d:\X_Files\Antigravity\Test_pdfcraft\01\REK GALANG JUL 2026.pdf")
    print("Paragraphs in original REK GALANG JUL 2026.pdf:")
    for p in client.get_paragraphs(doc_id, page=1):
        if p["rect"][1] < 150:
            print(f"P#{p['paragraph']:2d} rect={p['rect']} text={repr(p['text'])}")
    client.doc_close(doc_id, discard_changes=True)
