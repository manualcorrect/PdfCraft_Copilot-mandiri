import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf"

with PdfCraftClient() as client:
    doc_id = client.doc_open(pdf_path)
    paras = client.get_paragraphs(doc_id, page=1)
    print("Page 1 paragraphs near summary box (y between 150 and 260, x > 300):")
    for p in sorted(paras, key=lambda x: x["rect"][1]):
        if 150 <= p["rect"][1] <= 260 and p["rect"][0] > 300:
            print(f"  P{p['paragraph']}: rect={p['rect']}, text={p['text']!r}")
