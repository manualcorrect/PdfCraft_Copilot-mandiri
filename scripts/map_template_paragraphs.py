import os
import sys

sys.path.insert(0, r"C:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\src")
from pdfcraft_client import PdfCraftClient

with PdfCraftClient() as client:
    # 1. Inspect master_page_1
    d1 = client.doc_open(r"C:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\templates\master_page_1.pdf")
    paras1 = client.get_paragraphs(d1, page=1)
    print(f"=== master_page_1 (Total {len(paras1)}) ===")
    for p in paras1:
        txt = p["text"].strip()
        r = [round(x, 1) for x in p["rect"]]
        # Filter table or header
        if r[1] > 320 and any(k in txt for k in ["+", "-", "1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "0"]):
            print(f"P#{p['paragraph']:3d} | rect={r} | text={repr(txt[:35])}")
    client.doc_close(d1)

    # 2. Inspect master_page_intermediate
    d2 = client.doc_open(r"C:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\templates\master_page_intermediate.pdf")
    paras2 = client.get_paragraphs(d2, page=1)
    print(f"\n=== master_page_intermediate (Total {len(paras2)}) ===")
    for p in paras2:
        txt = p["text"].strip()
        r = [round(x, 1) for x in p["rect"]]
        if r[1] > 210 and any(k in txt for k in ["+", "-", "1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "0"]):
            print(f"P#{p['paragraph']:3d} | rect={r} | text={repr(txt[:35])}")
    client.doc_close(d2)
