import sys, os
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\2.pdf"
with PdfCraftClient() as client:
    doc_id = client.doc_open(pdf_path)
    paras = client.get_paragraphs(doc_id, page=1)
    for p in sorted(paras, key=lambda x: x['rect'][1]):
        r = p['rect']
        t = p['text'].strip()
        if r[1] >= 320 and r[0] < 50:
            print(f"P#{p['paragraph']:2d} rect={r} text={repr(t)}")
    client.doc_close(doc_id)
