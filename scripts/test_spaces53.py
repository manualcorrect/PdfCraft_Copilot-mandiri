import os
import sys
import shutil

sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient
import pdfplumber

ref3_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\3.pdf"

test_pdf = "output/test_spaces53.pdf"
shutil.copyfile(ref3_path, test_pdf)
with PdfCraftClient() as client:
    doc_id = client.doc_open(test_pdf)
    paras = client.get_paragraphs(doc_id, page=4)
    p25 = [p for p in paras if "83" in p["text"] and "Biaya" in p["text"]][0]
    
    # Test spaces
    spaces = " " * 53
    text_with_spaces = f"35{spaces}Biaya administrasi rekening"
    client.edit_text(doc_id, page=4, paragraph=p25["paragraph"], text=text_with_spaces, width=400.0)
    client.doc_save(doc_id, path=test_pdf, full=True)
    client.doc_close(doc_id)

with pdfplumber.open(test_pdf) as pdf:
    p4 = pdf.pages[3]
    chars = [c for c in p4.chars if 225 < c['top'] < 235 and c['x0'] < 140 and c['text'] not in ['2', '3', '8', '0', 'W', 'I', 'B', ':', ' ']]
    for c in chars:
        print(f"'{c['text']}' font={c.get('fontname')} x0={c['x0']:.2f} top={c['top']:.2f}")
