import sys, os
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\2.pdf"
with PdfCraftClient() as client:
    doc_id = client.doc_open(pdf_path)
    for p_num in range(1, 5):
        paras = client.get_paragraphs(doc_id, page=p_num)
        print(f"=== PAGE {p_num} ===")
        for p in paras:
            r = p['rect']
            t = p['text'].strip()
            if any(k in t for k in ['ROY DARWIN', 'Taman Aries', '01Jan', '09Sep', 'dari', 'of', '165000358', '445.950', '5.124.603', '4.700.000', '21.347']):
                print(f"  P#{p['paragraph']:2d} rect={r} text={repr(t)}")
    client.doc_close(doc_id)
