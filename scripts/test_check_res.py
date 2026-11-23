import sys
import os

sys.path.insert(0, r"C:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\src")
from pdfcraft_client import PdfCraftClient

with PdfCraftClient() as client:
    d = client.doc_open(r"D:\X_Files\rekening\Reference\Roy\ilovepdf_unlocked\Agu 2026_unlocked.pdf")
    res = client.call_tool("text_paragraphs", {"doc": d, "page": 1})
    print("res count:", res.get("count"))
    print("res paragraphs len:", len(res.get("paragraphs", [])))
    client.doc_close(d)
