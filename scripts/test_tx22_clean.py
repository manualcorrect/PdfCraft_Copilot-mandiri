import sys
sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient
import pdfplumber
import shutil

shutil.copyfile(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\REK_GALANG_AUG_2026_FINAL.pdf", "output/test_tx22_clean.pdf")

with PdfCraftClient() as client:
    doc = client.doc_open("output/test_tx22_clean.pdf")
    p22 = [p for p in client.get_paragraphs(doc, page=2) if abs(p["rect"][1] - 733.92) < 22 and 120 <= p["rect"][0] <= 135][0]
    
    text = "Transfer BI Fast\nDari BCA\nPT BENDI NASHA NIAGA INDUSTRI 5411078192\n(CENAIDJA)"
    # What if we pass width=200.0 or what if we check line by line?
    client.call_tool("text_edit", {
        "doc": doc, "page": 2, "paragraph": p22["paragraph"],
        "text": text,
        "line_spacing": 1.25
    })
    
    # Check rect
    up = [p for p in client.get_paragraphs(doc, page=2) if p["paragraph"] == p22["paragraph"]][0]
    print("Rect after text_edit without width:", up["rect"])
    print("Editor text:\n" + up.get("editor_text", ""))
    
    # Adjust position
    target_top = 733.92 - (len(text.split("\n")) - 1) * 5.0
    dx = 124.00 - up["rect"][0]
    dy = up["rect"][1] - target_top
    client.edit_text(doc, page=2, paragraph=p22["paragraph"], dx=dx, dy=dy)
    
    client.doc_save(doc, "output/test_tx22_clean.pdf", full=True)
    client.doc_close(doc)

with pdfplumber.open("output/test_tx22_clean.pdf") as pdf:
    words = [w for w in pdf.pages[1].extract_words() if abs(w['top'] - 733.92) < 25 and 120 <= w['x0'] <= 365]
    lines = {}
    for w in sorted(words, key=lambda x: (x['top'], x['x0'])):
        lines.setdefault(round(w['top'], 1), []).append(w['text'])
    print("\nResult in test_tx22_clean.pdf:")
    for top, ws in sorted(lines.items()):
        print(f"  top={top:5.1f}: {' '.join(ws)}")
