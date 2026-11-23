import sys
sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient

ref3_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\3.pdf"

with PdfCraftClient() as client:
    doc_id = client.doc_open(ref3_path)
    paras = client.get_paragraphs(doc_id, page=4)
    for p in paras:
        if p['rect'][1] < 280:
            print(f"P4 para {p['paragraph']}: rect={p['rect']}, text={repr(p['text'])}")
    client.doc_close(doc_id)
