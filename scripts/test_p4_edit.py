import os
import sys
import shutil

sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient
import pdfplumber

ref3_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\3.pdf"
test_pdf = "output/test_p4_edit.pdf"
shutil.copyfile(ref3_path, test_pdf)

with PdfCraftClient() as client:
    doc_id = client.doc_open(test_pdf)
    paras = client.get_paragraphs(doc_id, page=4)
    p25 = [p for p in paras if "83" in p["text"] and "Biaya" in p["text"]][0]
    print("Found p25:", p25)
    
    # Try editing text
    # What if we set text = "35         Biaya administrasi rekening"?
    # Or what if we add a new paragraph? Does client have page_add_text?
    client.doc_close(doc_id)
