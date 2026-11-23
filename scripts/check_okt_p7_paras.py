import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\okt\0.pdf"

with PdfCraftClient() as client:
    doc_id = client.doc_open(pdf_path)
    paras_p7 = client.get_paragraphs(doc_id, page=7)
    print("Page 7 paragraphs count:", len(paras_p7))
    for p in paras_p7:
        print(f"  Para {p['paragraph']:02d} rect={p['rect']}: text='{p['text'][:60]}...'")
    client.doc_close(doc_id)
