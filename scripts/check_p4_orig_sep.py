import sys
sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient

sep_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_SEP_2026.pdf"

with PdfCraftClient() as client:
    doc_id = client.doc_open(sep_path)
    paras_p4 = client.get_paragraphs(doc_id, page=4)
    print("--- Page 4 paras in REK_GALANG_SEP_2026.pdf ---")
    for p in paras_p4:
        if p["rect"][1] < 300:
            print(f"p{p['paragraph']}: rect={p['rect']}, text={repr(p['text'])}")
    client.doc_close(doc_id)
