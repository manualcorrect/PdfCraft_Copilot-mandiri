import sys
sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient

sep_rev = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_sep byk harus revisi.pdf"

with PdfCraftClient() as client:
    doc_id = client.doc_open(sep_rev)
    for p_num in range(1, 4):
        paras = client.get_paragraphs(doc_id, page=p_num)
        print(f"\n--- Page {p_num} paras in sep_rev ---")
        for p in paras:
            if p["rect"][1] > 320:
                print(f"p{p['paragraph']}: rect={p['rect']}, text={repr(p['text'])}")
    client.doc_close(doc_id)
