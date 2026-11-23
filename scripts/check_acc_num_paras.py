import sys
sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient
import pdfplumber

with PdfCraftClient() as client:
    doc = client.doc_open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\1.pdf")
    paras = client.get_paragraphs(doc, page=1)
    for p in paras:
        if any(k in p["text"] for k in ["1650", "1660", "Nomor", "Account", "Mata Uang", "IDR"]):
            print(f"P{p['paragraph']:2d}: {repr(p['text']):30s} rect={p['rect']}")
    client.doc_close(doc)

print("\n=== Chars in 1.pdf ===")
with pdfplumber.open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\1.pdf") as pdf:
    for c in pdf.pages[0].chars:
        if 20 <= c["x0"] <= 300 and 180 <= c["top"] <= 230:
            print(f"Char: {repr(c['text']):5s} x0={c['x0']:5.1f} top={c['top']:5.1f}")
