import os
import sys
import shutil

sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient
import pdfplumber

ref3_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\3.pdf"
test_pdf = "output/test_ref3_p4.pdf"
shutil.copyfile(ref3_path, test_pdf)

with PdfCraftClient() as client:
    doc_id = client.doc_open(test_pdf)
    paras = client.get_paragraphs(doc_id, page=4)
    p25 = [p for p in paras if "83" in p["text"] and "Biaya" in p["text"]][0]
    print("Editing p25 in test_ref3_p4...")
    # What if we set text="35" and width=30?
    client.edit_text(doc_id, page=4, paragraph=p25["paragraph"], text="35", width=30.0)
    
    # Can we call page_add_text on page 4?
    # Let's check call_tool with page_add_text
    try:
        res = client.call_tool("page_add_text", {
            "doc": doc_id,
            "page": 4,
            "text": "Biaya administrasi rekening",
            "at": [124.0, 228.0],
            "size": 8.0,
            "color": "#000000"
        })
        print("page_add_text success:", res)
    except Exception as e:
        print("page_add_text error:", e)
        
    client.doc_save(doc_id, path=test_pdf, full=True)
    client.doc_close(doc_id)

with pdfplumber.open(test_pdf) as pdf:
    p4 = pdf.pages[3]
    for c in p4.chars:
        if 220 < c['top'] < 240:
            print(f"c='{c['text']}' font={c.get('fontname')} x0={c['x0']:.2f} top={c['top']:.2f}")
