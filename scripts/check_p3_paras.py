import sys
sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient

with PdfCraftClient() as client:
    doc = client.doc_open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\1.pdf")
    paras = client.get_paragraphs(doc, page=3)
    for p in paras:
        if "Biaya" in p["text"] or "83" in p["text"] or "saldo" in p["text"]:
            print(p["paragraph"], repr(p["text"]), p["rect"])
    client.doc_close(doc)
