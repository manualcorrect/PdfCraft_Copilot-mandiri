import sys
sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient

with PdfCraftClient() as client:
    doc = client.doc_open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\1.pdf")
    paras = client.get_paragraphs(doc, page=1)
    for p in paras:
        if 140 <= p["rect"][0] <= 160 and 180 <= p["rect"][1] <= 220:
            print(f"P{p['paragraph']}: {repr(p['text'])} rect={p['rect']}")
    client.doc_close(doc)
