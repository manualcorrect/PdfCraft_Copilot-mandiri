import sys
sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient
import pdfplumber

with PdfCraftClient() as client:
    doc_id = client.doc_open("output/test_no_width.pdf")
    # Let's test on page 2 paragraph 89
    paras = client.get_paragraphs(doc_id, page=2)
    p22 = [p for p in paras if "BENDI" in p["text"]][0]
    
    # Try different widths: 150, 160, 170, 175
    text = "Transfer BI Fast\nDari BCA\nPT BENDI NASHA NIAGA INDUSTRI 5411078192\n(CENAIDJA)"
    # What if we pass width=175.0?
    # "Transfer BI Fast" (60 pt) -> fits
    # "Dari BCA" (35 pt) -> fits
    # "PT BENDI NASHA NIAGA INDUSTRI 5411078192" (167.5 pt) -> fits in 175 pt!
    # "(CENAIDJA)" (45 pt) -> fits
    client.call_tool("text_edit", {
        "doc": doc_id,
        "page": 2,
        "paragraph": p22["paragraph"],
        "text": text,
        "width": 175.0,
        "line_spacing": 1.25
    })
    
    client.doc_save(doc_id, path="output/test_width_175.pdf", full=True)
    client.doc_close(doc_id)

with pdfplumber.open("output/test_width_175.pdf") as pdf:
    p2 = pdf.pages[1]
    words = [w for w in p2.extract_words() if abs(w['top'] - 733.92) < 25 and 120 <= w['x0'] <= 365]
    lines = {}
    for w in sorted(words, key=lambda x: (x['top'], x['x0'])):
        lines.setdefault(round(w['top'], 1), []).append(w['text'])
    print("Resulting lines with width=175.0:")
    for top, ws in sorted(lines.items()):
        print(f"  top={top:5.1f}: {' '.join(ws)}")
