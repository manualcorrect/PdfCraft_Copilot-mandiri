import os
import sys
import shutil

sys.path.insert(0, os.path.abspath("src"))
from pdfcraft_client import PdfCraftClient
import pdfplumber

src_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\REK_GALANG_AUG_2026_FINAL.pdf"
test_pdf = "output/test_no_width.pdf"
shutil.copyfile(src_pdf, test_pdf)

with PdfCraftClient() as client:
    doc_id = client.doc_open(test_pdf)
    paras = client.get_paragraphs(doc_id, page=2)
    p22 = [p for p in paras if abs(p["rect"][1] - 733.92) < 22 and 120 <= p["rect"][0] <= 135][0]
    
    text = "Transfer BI Fast\nDari BCA\nPT BENDI NASHA NIAGA INDUSTRI 5411078192\n(CENAIDJA)"
    client.call_tool("text_edit", {
        "doc": doc_id,
        "page": 2,
        "paragraph": p22["paragraph"],
        "text": text,
        "line_spacing": 1.25
    })
    
    # Check rect
    up = [p for p in client.get_paragraphs(doc_id, page=2) if p["paragraph"] == p22["paragraph"]][0]
    print("Rect without width:", up["rect"])
    
    # target_top for 4 lines is 733.92 - 15 = 718.92
    dy = up["rect"][1] - 718.92
    dx = 124.00 - up["rect"][0]
    client.edit_text(doc_id, page=2, paragraph=p22["paragraph"], dx=dx, dy=dy)
    
    client.doc_save(doc_id, path=test_pdf, full=True)
    client.doc_close(doc_id)

with pdfplumber.open(test_pdf) as pdf:
    p2 = pdf.pages[1]
    words = [w for w in p2.extract_words() if abs(w['top'] - 733.92) < 22 and 120 <= w['x0'] <= 365]
    lines = {}
    for w in sorted(words, key=lambda x: (x['top'], x['x0'])):
        lines.setdefault(round(w['top'], 1), []).append(w['text'])
    print("\nResulting lines:")
    for top, ws in sorted(lines.items()):
        print(f"  top={top:5.1f}: {' '.join(ws)}")
