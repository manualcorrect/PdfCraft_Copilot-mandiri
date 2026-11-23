import sys
sys.path.insert(0, "src")
import shutil
from pdfcraft_client import PdfCraftClient
import pdfplumber

shutil.copyfile(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\1.pdf", "output/test_okt.pdf")

with PdfCraftClient() as client:
    doc = client.doc_open("output/test_okt.pdf")
    paras = client.get_paragraphs(doc, page=1)
    
    # 1. Edit Periode to "01 Okt 2026 - 31 Okt 2026"
    p_per = [p for p in paras if "01 Jan 2026" in p["text"] and 90 <= p["rect"][1] <= 115][0]
    client.call_tool("text_edit", {
        "doc": doc, "page": 1, "paragraph": p_per["paragraph"], "text": "01 Okt 2026 - 31 Okt 2026"
    })
    
    # 2. Edit Date Row 1 to "01 Okt 2026"
    paras = client.get_paragraphs(doc, page=1)
    p_d1 = [p for p in paras if 45 <= p["rect"][0] <= 85 and abs(p["rect"][1] - 340) < 10 and "WIB" not in p["text"]][0]
    client.call_tool("text_edit", {
        "doc": doc, "page": 1, "paragraph": p_d1["paragraph"], "text": "01 Okt 2026"
    })
    
    client.doc_save(doc, path="output/test_okt.pdf", full=True)
    client.doc_close(doc)

with pdfplumber.open("output/test_okt.pdf") as pdf:
    print("=== Chars in Periode ===")
    for c in pdf.pages[0].chars:
        if 320 <= c["x0"] <= 450 and abs(c["top"] - 100) < 15:
            print(f"Char: {repr(c['text']):5s} font={c['fontname']} adv={c.get('adv')}")

    print("\n=== Chars in Date Row 1 ===")
    for c in pdf.pages[0].chars:
        if 45 <= c["x0"] <= 95 and abs(c["top"] - 340) < 15:
            print(f"Char: {repr(c['text']):5s} font={c['fontname']} adv={c.get('adv')}")
