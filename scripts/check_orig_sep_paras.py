import sys
sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient

sep_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_SEP_2026.pdf"

with PdfCraftClient() as client:
    doc_id = client.doc_open(sep_path)
    paras_p2 = client.get_paragraphs(doc_id, page=2)
    print("--- Page 2 paras near 550 in REK_GALANG_SEP_2026.pdf ---")
    for p in paras_p2:
        if 530 < p["rect"][1] < 570:
            print(f"p{p['paragraph']}: rect={p['rect']}, text={repr(p['text'])}")
            
    paras_p3 = client.get_paragraphs(doc_id, page=3)
    print("\n--- Page 3 paras near 734 in REK_GALANG_SEP_2026.pdf ---")
    for p in paras_p3:
        if 715 < p["rect"][1] < 755:
            print(f"p{p['paragraph']}: rect={p['rect']}, text={repr(p['text'])}")
    client.doc_close(doc_id)
