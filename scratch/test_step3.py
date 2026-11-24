import sys
import os
import shutil
import re
import zlib

sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient

pdf_src = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\aug\0.pdf"
pdf_test = r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\scratch\test_wafiq_step3.pdf"
shutil.copyfile(pdf_src, pdf_test)

with PdfCraftClient() as client:
    doc_id = client.doc_open(pdf_test)
    client.edit_text(doc_id, page=1, paragraph=3, text="Nama/Name") # dummy edit or header edit
    client.doc_save(doc_id, pdf_test)
    client.doc_close(doc_id)

with open(pdf_test, "rb") as f:
    pdf_bytes = f.read()

sx_matches = re.findall(rb"startxref[\r\n]+(\d+)", pdf_bytes)
print("startxref matches:", sx_matches)
for sx in sx_matches:
    offset = int(sx)
    print(f"Checking offset {offset}:")
    chunk = pdf_bytes[max(0, offset-50):offset+200]
    print(chunk[:100])
