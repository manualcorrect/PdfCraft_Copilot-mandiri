import sys
import os
sys.path.append(os.path.abspath("src"))
sys.stdout.reconfigure(encoding='utf-8')
from pdfcraft_client import PdfCraftClient

with PdfCraftClient() as client:
    doc_id = client.doc_open("templates/master_page_intermediate.pdf")
    lines = client.call_tool("text_lines", {"doc": doc_id, "page": 1}).get("lines", [])
    print("Lines in master_page_intermediate.pdf:")
    for l in lines:
        if l["rect"][1] < 140:
            print(f"  {l['rect']}: {repr(l['text'])}")
    paras = client.get_paragraphs(doc_id, page=1)
    print("\nParas in master_page_intermediate.pdf:")
    for p in paras:
        if p["rect"][1] < 140:
            print(f"  P#{p['paragraph']:2d} rect={p['rect']} text={repr(p['text'])}")
    client.doc_close(doc_id, discard_changes=True)
