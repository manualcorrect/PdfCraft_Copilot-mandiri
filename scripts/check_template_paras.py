import sys
import os
sys.path.append(os.path.abspath("src"))
sys.stdout.reconfigure(encoding='utf-8')
from pdfcraft_client import PdfCraftClient

with PdfCraftClient() as client:
    doc_id = client.doc_open("templates/master_page_1.pdf")
    paras = client.get_paragraphs(doc_id, page=1)
    print("Paragraphs in master_page_1.pdf around header:")
    for p in paras:
        rect = p["rect"]
        if rect[1] < 150:
            print(f"P#{p['paragraph']:2d} rect={rect} text={repr(p['text'])}")
    client.doc_close(doc_id)
