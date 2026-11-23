import sys
sys.path.insert(0, "src")
import shutil
from pdfcraft_client import PdfCraftClient
import pdfplumber

shutil.copyfile(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\1.pdf", "output/test_oct_font.pdf")

with PdfCraftClient() as client:
    doc = client.doc_open("output/test_oct_font.pdf")
    paras = client.get_paragraphs(doc, page=1)
    
    # Let's test editing row 1 date: paragraph for '01 Jan 2026'
    # Find paragraph
    p_date = [p for p in paras if "01 Jan 2026" in p["text"]][0]
    print("Editing paragraph:", p_date["paragraph"], p_date["text"])
    
    # Test A: edit with font="helvetica"
    res = client.call_tool("text_edit", {
        "doc": doc,
        "page": 1,
        "paragraph": p_date["paragraph"],
        "text": "01 Oct 2026",
        "font": "helvetica"
    })
    print("Result with font=helvetica:", res)
    
    client.doc_save(doc, path="output/test_oct_font.pdf", full=True)
    client.doc_close(doc)

with pdfplumber.open("output/test_oct_font.pdf") as pdf:
    print("=== Chars at top=100 (Periode) ===")
    for c in pdf.pages[0].chars:
        if 320 <= c["x0"] <= 420 and abs(c["top"] - 100) < 15:
            print(f"Char: {repr(c['text']):8s} font={c['fontname']} adv={c.get('adv')}")
