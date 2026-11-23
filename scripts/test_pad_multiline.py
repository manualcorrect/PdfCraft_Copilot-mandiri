import os
import sys
import shutil

sys.path.insert(0, os.path.abspath("src"))
from pdfcraft_client import PdfCraftClient
import pdfplumber

src_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\REK_GALANG_AUG_2026_FINAL.pdf"
test_pdf = "output/test_forced_breaks.pdf"
shutil.copyfile(src_pdf, test_pdf)

with pdfplumber.open(src_pdf) as pdf:
    char_widths = {}
    for p in pdf.pages:
        for c in p.chars:
            if c.get("size") == 8.0:
                char_widths[c["text"]] = c["width"]
if " " not in char_widths: char_widths[" "] = 2.2

def get_text_width(text):
    return sum(char_widths.get(ch, 4.5) for ch in text)

def pad_multiline(lines, target_width):
    space_w = char_widths.get(" ", 2.2)
    result = []
    for i, l in enumerate(lines):
        l_str = l.strip()
        if i < len(lines) - 1:
            curr_w = get_text_width(l_str)
            needed = int((target_width - curr_w) / space_w) + 2
            result.append(l_str + (" " * max(1, needed)))
        else:
            result.append(l_str)
    return "\n".join(result)

# Test on Tx 22 (Salary) and Tx 03
with PdfCraftClient() as client:
    doc_id = client.doc_open(test_pdf)
    
    # 1. Tx 22 (Page 2, Row 12, row_y=733.92)
    p2_paras = client.get_paragraphs(doc_id, page=2)
    p22 = [p for p in p2_paras if abs(p["rect"][1] - 733.92) < 22 and 120 <= p["rect"][0] <= 135][0]
    
    lines_22 = [
        "Transfer BI Fast",
        "Dari BCA",
        "PT BENDI NASHA NIAGA INDUSTRI 5411078192",
        "(CENAIDJA)"
    ]
    width_22 = max(get_text_width(l) for l in lines_22) + 5.0 # ~173 pt
    text_22 = pad_multiline(lines_22, width_22)
    target_top_22 = 733.92 - (len(lines_22) - 1) * 5.0 # 718.92
    
    client.call_tool("text_edit", {
        "doc": doc_id, "page": 2, "paragraph": p22["paragraph"],
        "text": text_22, "width": width_22, "line_spacing": 1.25
    })
    up22 = [p for p in client.get_paragraphs(doc_id, page=2) if p["paragraph"] == p22["paragraph"]][0]
    dx = 124.00 - up22["rect"][0]
    dy = up22["rect"][1] - target_top_22
    client.edit_text(doc_id, page=2, paragraph=p22["paragraph"], dx=dx, dy=dy)
    
    # 2. Tx 03 (Page 1, Row 3, row_y=435.92)
    p1_paras = client.get_paragraphs(doc_id, page=1)
    p3 = [p for p in p1_paras if abs(p["rect"][1] - 435.92) < 22 and 120 <= p["rect"][0] <= 135][0]
    lines_3 = [
        "Pembayaran QR",
        "ke SOTO AYAM LAMONGAN CAK JO",
        "601483798729"
    ]
    width_3 = max(get_text_width(l) for l in lines_3) + 5.0
    text_3 = pad_multiline(lines_3, width_3)
    target_top_3 = 435.92 - (len(lines_3) - 1) * 5.0
    
    client.call_tool("text_edit", {
        "doc": doc_id, "page": 1, "paragraph": p3["paragraph"],
        "text": text_3, "width": width_3, "line_spacing": 1.25
    })
    up3 = [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == p3["paragraph"]][0]
    dx = 124.00 - up3["rect"][0]
    dy = up3["rect"][1] - target_top_3
    client.edit_text(doc_id, page=1, paragraph=p3["paragraph"], dx=dx, dy=dy)

    client.doc_save(doc_id, path=test_pdf, full=True)
    client.doc_close(doc_id)

with pdfplumber.open(test_pdf) as pdf:
    print("--- Tx 03 (Page 1) ---")
    w3 = [w for w in pdf.pages[0].extract_words() if abs(w['top'] - 435.92) < 22 and 120 <= w['x0'] <= 365]
    l3 = {}
    for w in sorted(w3, key=lambda x: (x['top'], x['x0'])):
        l3.setdefault(round(w['top'], 1), []).append(w['text'])
    for top, ws in sorted(l3.items()):
        print(f"  top={top:5.1f}: {' '.join(ws)}")

    print("\n--- Tx 22 (Page 2) ---")
    w22 = [w for w in pdf.pages[1].extract_words() if abs(w['top'] - 733.92) < 25 and 120 <= w['x0'] <= 365]
    l22 = {}
    for w in sorted(w22, key=lambda x: (x['top'], x['x0'])):
        l22.setdefault(round(w['top'], 1), []).append(w['text'])
    for top, ws in sorted(l22.items()):
        print(f"  top={top:5.1f}: {' '.join(ws)}")
