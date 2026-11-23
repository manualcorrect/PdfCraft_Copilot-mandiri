import sys
sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient

with PdfCraftClient() as client:
    doc = client.doc_open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\REK_GALANG_AUG_2026_FINAL.pdf")
    p22 = [p for p in client.get_paragraphs(doc, page=2) if abs(p['rect'][1] - 733.92) < 22 and 120 <= p['rect'][0] <= 135][0]
    print("p22 lines:", p22.get("lines"))
    print("p22 rows:", p22.get("rows"))
    client.doc_close(doc)
