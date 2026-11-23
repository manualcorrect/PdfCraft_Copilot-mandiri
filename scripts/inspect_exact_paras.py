import sys
sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient

sep_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_SEP_2026.pdf"

with PdfCraftClient() as client:
    doc_id = client.doc_open(sep_path)
    for p_num in range(1, 5):
        paras = client.get_paragraphs(doc_id, page=p_num)
        print(f"\n==================== PAGE {p_num} ====================")
        for p in paras:
            if p["rect"][1] > 200:
                print(f"p{p['paragraph']}: rect={p['rect']}, text={repr(p['text'])}")
    client.doc_close(doc_id)
