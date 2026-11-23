import sys
sys.path.insert(0, "src")
import shutil
from pdfcraft_client import PdfCraftClient
import pdfplumber

test_pdf = "output/test_oct_clean.pdf"
shutil.copyfile(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\1.pdf", test_pdf)

with PdfCraftClient() as client:
    doc = client.doc_open(test_pdf)
    
    # 1. Header on Page 1
    paras = client.get_paragraphs(doc, page=1)
    
    # Cabang empty
    p_cabang = [p for p in paras if "Taman Aries" in p["text"]][0]
    client.call_tool("text_edit", {"doc": doc, "page": 1, "paragraph": p_cabang["paragraph"], "text": ""})
    
    # Name + Cabang composite with font="helvetica"
    paras = client.get_paragraphs(doc, page=1)
    p_name = [p for p in paras if "ROY DARWIN" in p["text"]][0]
    client.call_tool("text_edit", {
        "doc": doc, "page": 1, "paragraph": p_name["paragraph"],
        "text": "GALANG PUTRA\nKURNIAWAN\nKCP Serang Ciceri",
        "line_spacing": 1.375,
        "font": "helvetica"
    })
    
    # Periode: "01 Okt 2026 - 31 Okt 2026"
    paras = client.get_paragraphs(doc, page=1)
    p_per = [p for p in paras if "01 Jan" in p["text"] and 90 <= p["rect"][1] <= 115][0]
    client.call_tool("text_edit", {
        "doc": doc, "page": 1, "paragraph": p_per["paragraph"],
        "text": "01 Okt 2026 - 31 Okt 2026"
    })
    
    # Dicetak Pada: "05 Nov 2026"
    paras = client.get_paragraphs(doc, page=1)
    p_dic = [p for p in paras if "09 Sep 2026" in p["text"] and 115 <= p["rect"][1] <= 135][0]
    client.call_tool("text_edit", {
        "doc": doc, "page": 1, "paragraph": p_dic["paragraph"],
        "text": "05 Nov 2026"
    })
    
    # Page numbers: "1 dari 4", "1 of 4"
    paras = client.get_paragraphs(doc, page=1)
    for p in paras:
        if p["text"].strip().isdigit() and 545 <= p["rect"][0] <= 575 and 90 <= p["rect"][1] <= 110:
            client.call_tool("text_edit", {"doc": doc, "page": 1, "paragraph": p["paragraph"], "text": ""})
            
    paras = client.get_paragraphs(doc, page=1)
    for p in paras:
        if "dari" in p["text"] and 520 <= p["rect"][0] <= 570 and 90 <= p["rect"][1] <= 115:
            client.call_tool("text_edit", {"doc": doc, "page": 1, "paragraph": p["paragraph"], "text": "1 dari 4", "width": 50.0})
        elif "of" in p["text"] and 530 <= p["rect"][0] <= 570 and 105 <= p["rect"][1] <= 125:
            client.call_tool("text_edit", {
                "doc": doc, "page": 1, "paragraph": p["paragraph"],
                "text": "1 of 4", "width": 50.0, "font": "helvetica", "italic": True
            })
            
    # Dates on Page 1: replace Jan with Okt
    paras = client.get_paragraphs(doc, page=1)
    for p in paras:
        if 45 <= p["rect"][0] <= 85 and 320 <= p["rect"][1] <= 780 and "WIB" not in p["text"] and "Jan" in p["text"]:
            new_t = p["text"].replace("Jan", "Okt").replace("01Jan", "01 Okt").replace("03Jan", "03 Okt")
            client.call_tool("text_edit", {"doc": doc, "page": 1, "paragraph": p["paragraph"], "text": new_t})

    client.doc_save(doc, path=test_pdf, full=True)
    
    # Render preview
    render_res = client.call_tool("page_render", {"doc": doc, "page": 1, "dpi": 150})
    print("Render result:", render_res.get("path") or render_res)
    client.doc_close(doc)

print("\n=== Verifying text on Page 1 ===")
with pdfplumber.open(test_pdf) as pdf:
    print(pdf.pages[0].extract_text()[:600])
