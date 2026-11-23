import sys
sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient

sep_rev = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_sep byk harus revisi.pdf"

with PdfCraftClient() as client:
    doc_id = client.doc_open(sep_rev)
    paras = client.get_paragraphs(doc_id, page=4)
    print("Page 4 paras in sep_rev:")
    for p in paras:
        if p['rect'][1] < 300:
            print(f"  para {p['paragraph']}: rect={p['rect']}, text={repr(p['text'])}")
    client.doc_close(doc_id)
