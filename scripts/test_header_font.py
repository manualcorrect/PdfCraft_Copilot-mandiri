import sys
sys.path.insert(0, "src")
import shutil
from pdfcraft_client import PdfCraftClient
import pdfplumber

shutil.copyfile(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\1.pdf", "output/test_header_font.pdf")

with PdfCraftClient() as client:
    doc = client.doc_open("output/test_header_font.pdf")
    paras = client.get_paragraphs(doc, page=1)
    
    # Empty old cabang
    p_cabang = [p for p in paras if "Taman Aries" in p["text"]][0]
    client.call_tool("text_edit", {"doc": doc, "page": 1, "paragraph": p_cabang["paragraph"], "text": ""})
    
    # Edit p_name with font="helvetica"
    paras = client.get_paragraphs(doc, page=1)
    p_name = [p for p in paras if "ROY DARWIN" in p["text"]][0]
    client.call_tool("text_edit", {
        "doc": doc,
        "page": 1,
        "paragraph": p_name["paragraph"],
        "text": "GALANG PUTRA\nKURNIAWAN\nKCP Serang Ciceri",
        "line_spacing": 1.375,
        "font": "helvetica"
    })
    
    client.doc_save(doc, path="output/test_header_font.pdf", full=True)
    client.doc_close(doc)

with pdfplumber.open("output/test_header_font.pdf") as pdf:
    print("=== Chars in Header Name & Cabang ===")
    for c in pdf.pages[0].chars:
        if 110 <= c["x0"] <= 250 and 90 <= c["top"] <= 140:
            print(f"Char: {repr(c['text']):5s} font={c['fontname']} size={c['size']} x0={c['x0']:.1f} top={c['top']:.1f}")
