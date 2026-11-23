import os
import sys
import shutil

sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient
import pdfplumber

ref3_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\3.pdf"
test_pdf = "output/test_edit_all_in_ref3.pdf"
shutil.copyfile(ref3_path, test_pdf)

with PdfCraftClient() as client:
    doc_id = client.doc_open(test_pdf)
    
    # 1. Page 2, Row 18: In 3.pdf, what is paragraph for Row 18?
    paras_p2 = client.get_paragraphs(doc_id, page=2)
    # Row 18 row_y = 227.92 + 7 * 46.00 = 549.92
    p_r18 = [p for p in paras_p2 if abs(p["rect"][1] - 549.92) < 20 and 120 <= p["rect"][0] <= 135]
    print("Page 2 Row 18 paras:", p_r18)
    if p_r18:
        client.edit_text(doc_id, page=2, paragraph=p_r18[0]["paragraph"], text="Biaya transfer BI Fast")
        
    # 2. Page 3, Row 34: row_y = 227.92 + 11 * 46.00 = 733.92
    paras_p3 = client.get_paragraphs(doc_id, page=3)
    p_r34 = [p for p in paras_p3 if abs(p["rect"][1] - 733.92) < 20 and 120 <= p["rect"][0] <= 135]
    print("Page 3 Row 34 paras:", p_r34)
    if p_r34:
        client.edit_text(doc_id, page=3, paragraph=p_r34[0]["paragraph"], text="Penarikan tunai di ATM\nBANK MANDIRI SRG IM CIRUAS 01", line_spacing=1.25)
        
    client.doc_save(doc_id, path=test_pdf, full=True)
    client.doc_close(doc_id)

with pdfplumber.open(test_pdf) as pdf:
    for p_idx in [1, 2]:
        p = pdf.pages[p_idx]
        foreign = [c for c in p.chars if 'TTInterphases' not in c.get('fontname', '')]
        print(f"Page {p_idx+1} foreign font chars count: {len(foreign)}")
