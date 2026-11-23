import os
import sys
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from pdfcraft_client import PdfCraftClient

src = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\2.pdf"
test_out = r"output\test_edit_2pdf.pdf"
shutil.copyfile(src, test_out)

with PdfCraftClient() as client:
    doc_id = client.doc_open(test_out)
    paras = client.get_paragraphs(doc_id, page=1)
    print("Page 1 paragraphs count:", len(paras))
    for p in paras[:15]:
        print(f"  P{p['paragraph']}: y0={p['rect'][1]:.1f}, x0={p['rect'][0]:.1f}, text={repr(p['text'])[:50]}")
    client.doc_close(doc_id)
