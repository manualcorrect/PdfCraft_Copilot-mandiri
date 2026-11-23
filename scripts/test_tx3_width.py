import sys
sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient
import pdfplumber

with PdfCraftClient() as client:
    doc_id = client.doc_open("output/test_aug_keterangan_alignment.pdf")
    paras = client.get_paragraphs(doc_id, page=1)
    p3 = [p for p in paras if abs(p["rect"][1] - 435.92) < 22 and 120 <= p["rect"][0] <= 135][0]
    
    # "Pembayaran QR" (60 pt)
    # "ke SOTO AYAM LAMONGAN CAK JO" (130 pt)
    # "601483798729" (55 pt)
    # If width is 150.0:
    text = "Pembayaran QR\nke SOTO AYAM LAMONGAN CAK JO\n601483798729"
    client.call_tool("text_edit", {
        "doc": doc_id,
        "page": 1,
        "paragraph": p3["paragraph"],
        "text": text,
        "width": 150.0,
        "line_spacing": 1.25
    })
    
    # target top for 3 lines: 435.92 - 10 = 425.92
    up = [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == p3["paragraph"]][0]
    dy = up["rect"][1] - 425.92
    dx = 124.00 - up["rect"][0]
    client.edit_text(doc_id, page=1, paragraph=p3["paragraph"], dx=dx, dy=dy)
    
    client.doc_save(doc_id, path="output/test_p3_width.pdf", full=True)
    client.doc_close(doc_id)

with pdfplumber.open("output/test_p3_width.pdf") as pdf:
    p1 = pdf.pages[0]
    words = [w for w in p1.extract_words() if abs(w['top'] - 435.92) < 22 and 120 <= w['x0'] <= 365]
    lines = {}
    for w in sorted(words, key=lambda x: (x['top'], x['x0'])):
        lines.setdefault(round(w['top'], 1), []).append(w['text'])
    print("Resulting lines for Tx 03 with width=150.0:")
    for top, ws in sorted(lines.items()):
        print(f"  top={top:5.1f}: {' '.join(ws)}")
