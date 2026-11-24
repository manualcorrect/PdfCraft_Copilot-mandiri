import sys
import os
import shutil

sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient

pdf_src = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\aug\0.pdf"
pdf_test = r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\scratch\test_wafiq.pdf"
shutil.copyfile(pdf_src, pdf_test)

with PdfCraftClient() as client:
    doc_id = client.doc_open(pdf_test)
    print("Doc opened, ID:", doc_id)
    for p_num in range(1, 4):
        paras = client.get_paragraphs(doc_id, page=p_num)
        print(f"\n--- PAGE {p_num} ({len(paras)} paragraphs) ---")
        for p in paras[:8]:
            print(f"  Para {p['paragraph']}: '{p['text']}' rect={p['rect']}")
        print("  ...")
        for p in paras[-5:]:
            print(f"  Para {p['paragraph']}: '{p['text']}' rect={p['rect']}")
    client.doc_close(doc_id)
