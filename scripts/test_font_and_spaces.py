import os
import sys
import shutil

sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient
import pdfplumber

ref3_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\3.pdf"

# Test 1: page_add_text with font
test1_pdf = "output/test_font_add.pdf"
shutil.copyfile(ref3_path, test1_pdf)
with PdfCraftClient() as client:
    doc_id = client.doc_open(test1_pdf)
    try:
        res = client.call_tool("page_add_text", {
            "doc": doc_id,
            "page": 4,
            "text": "Biaya administrasi rekening",
            "at": [124.0, 228.0],
            "size": 8.0,
            "font": "IWUSEV+PDF-PDF-TTInterphases-",
            "color": "#000000"
        })
        print("page_add_text with font success:", res)
    except Exception as e:
        print("page_add_text with font error:", e)
    client.doc_save(doc_id, path=test1_pdf, full=True)
    client.doc_close(doc_id)

with pdfplumber.open(test1_pdf) as pdf:
    p4 = pdf.pages[3]
    for c in p4.chars:
        if c['text'] == 'B' and c['top'] > 220:
            print(f"Test 1 'B': font={c.get('fontname')}, x0={c['x0']:.2f}")

# Test 2: edit_text with spaces in p25
test2_pdf = "output/test_spaces.pdf"
shutil.copyfile(ref3_path, test2_pdf)
with PdfCraftClient() as client:
    doc_id = client.doc_open(test2_pdf)
    paras = client.get_paragraphs(doc_id, page=4)
    p25 = [p for p in paras if "83" in p["text"] and "Biaya" in p["text"]][0]
    # In TTInterphases, space is approx 2.2 pt width.
    # From x=29.28 to x=124.00 is 94.72 pt.
    # 94.72 / 2.2 approx 43 spaces!
    spaces = " " * 43
    text_with_spaces = f"35{spaces}Biaya administrasi rekening"
    client.edit_text(doc_id, page=4, paragraph=p25["paragraph"], text=text_with_spaces, width=350.0)
    client.doc_save(doc_id, path=test2_pdf, full=True)
    client.doc_close(doc_id)

with pdfplumber.open(test2_pdf) as pdf:
    p4 = pdf.pages[3]
    chars = [c for c in p4.chars if 225 < c['top'] < 235 and c['x0'] < 140]
    print("\nTest 2 chars:")
    for c in chars:
        print(f"  '{c['text']}' font={c.get('fontname')} x0={c['x0']:.2f} top={c['top']:.2f}")
