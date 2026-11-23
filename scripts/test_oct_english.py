import sys
sys.path.insert(0, "src")
import shutil
import base64
from pdfcraft_client import PdfCraftClient
from PIL import Image

test_pdf = "output/test_oct_english.pdf"
shutil.copyfile(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\1.pdf", test_pdf)

with PdfCraftClient() as client:
    doc = client.doc_open(test_pdf)
    paras = client.get_paragraphs(doc, page=1)
    
    # 1. Header Name + Cabang
    p_cabang = [p for p in paras if "Taman Aries" in p["text"]][0]
    client.call_tool("text_edit", {"doc": doc, "page": 1, "paragraph": p_cabang["paragraph"], "text": ""})
    
    paras = client.get_paragraphs(doc, page=1)
    p_name = [p for p in paras if "ROY DARWIN" in p["text"]][0]
    client.call_tool("text_edit", {
        "doc": doc, "page": 1, "paragraph": p_name["paragraph"],
        "text": "GALANG PUTRA\nKURNIAWAN\nKCP Serang Ciceri",
        "line_spacing": 1.375,
        "font": "helvetica"
    })
    
    # 2. Periode: "01 Oct 2026 - 31 Oct 2026" with font="helvetica"
    paras = client.get_paragraphs(doc, page=1)
    p_per = [p for p in paras if "01 Jan" in p["text"] and 90 <= p["rect"][1] <= 115][0]
    client.call_tool("text_edit", {
        "doc": doc, "page": 1, "paragraph": p_per["paragraph"],
        "text": "01 Oct 2026 - 31 Oct 2026",
        "font": "helvetica"
    })
    
    # 3. Dicetak Pada: "05 Nov 2026"
    paras = client.get_paragraphs(doc, page=1)
    p_dic = [p for p in paras if "09 Sep 2026" in p["text"] and 115 <= p["rect"][1] <= 135][0]
    client.call_tool("text_edit", {
        "doc": doc, "page": 1, "paragraph": p_dic["paragraph"],
        "text": "05 Nov 2026"
    })
    
    # 4. Page numbers: "1 dari 4", "1 of 4"
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
            
    # 5. Dates on Page 1: replace Jan with Oct and specify font="helvetica"
    paras = client.get_paragraphs(doc, page=1)
    for p in paras:
        if 45 <= p["rect"][0] <= 85 and 320 <= p["rect"][1] <= 780 and "WIB" not in p["text"] and "Jan" in p["text"]:
            new_t = p["text"].replace("Jan", "Oct").replace("01Jan", "01 Oct").replace("03Jan", "03 Oct")
            client.call_tool("text_edit", {
                "doc": doc, "page": 1, "paragraph": p["paragraph"],
                "text": new_t,
                "font": "helvetica"
            })

    client.doc_save(doc, path=test_pdf, full=True)
    
    # Render preview
    res = client.call_tool("page_render", {"doc": doc, "page": 1, "dpi": 150})
    b64_data = res["content"][0]["data"]
    with open("output/test_oct_english.png", "wb") as f:
        f.write(base64.b64decode(b64_data))
    client.doc_close(doc)

im = Image.open("output/test_oct_english.png")
w, h = im.size
crop1 = im.crop((0, 0, w, int(h * 0.4)))
crop1.save("C:/Users/Wisnu/.gemini/antigravity/brain/5e8306ab-a513-43f6-bf81-265c0e523098/oct_eng_header.png")
crop2 = im.crop((0, int(h * 0.4), w, int(h * 0.75)))
crop2.save("C:/Users/Wisnu/.gemini/antigravity/brain/5e8306ab-a513-43f6-bf81-265c0e523098/oct_eng_tx.png")
print("Rendered and saved english Oct crops successfully!")
