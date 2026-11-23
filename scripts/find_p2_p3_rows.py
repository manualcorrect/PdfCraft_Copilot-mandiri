import sys
sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient

ref3_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\3.pdf"

with PdfCraftClient() as client:
    doc_id = client.doc_open(ref3_path)
    print("--- Page 2 paras near 550 ---")
    paras_p2 = client.get_paragraphs(doc_id, page=2)
    for p in paras_p2:
        if 530 < p["rect"][1] < 570:
            print(f"p{p['paragraph']}: rect={p['rect']}, text={repr(p['text'])}")
            
    print("\n--- Page 3 paras near 734 ---")
    paras_p3 = client.get_paragraphs(doc_id, page=3)
    for p in paras_p3:
        if 715 < p["rect"][1] < 755:
            print(f"p{p['paragraph']}: rect={p['rect']}, text={repr(p['text'])}")
    client.doc_close(doc_id)
