import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from pdfcraft_client import PdfCraftClient
import pdfplumber

# Let's test Possibility A on master_page_1.pdf:
# Multi-line description for row 1: 3 lines
with PdfCraftClient() as client:
    doc_id = client.doc_open("templates/master_page_1.pdf")
    # In master_page_1, row 1 p_desc is paragraph 46 or 47?
    paras = client.get_paragraphs(doc_id, page=1)
    p_desc = [p for p in paras if abs(p["rect"][1] - 343.92) < 15 and 120 <= p["rect"][0] <= 135][0]
    print(f"p_desc before edit: y0={p_desc['rect'][1]:.2f}, text={repr(p_desc['text'])}")
    
    # 3 lines description:
    test_desc = "Biaya transaksi bank\nPembayaran Danatopup\n89508089622130569"
    # To place line 1 at y0=334.0 instead of 343.92, dy = 343.92 - 334.0 = +9.92 pt (up)
    # line_spacing in points = 10 pt / 8 pt = 1.25
    client.call_tool("text_edit", {
        "doc": doc_id,
        "page": 1,
        "paragraph": p_desc["paragraph"],
        "text": test_desc,
        "dy": 9.92,
        "line_spacing": 1.25,
        "width": 230.0
    })
    
    client.doc_save(doc_id, path="output/test_dy_desc.pdf")
    client.doc_close(doc_id)

with pdfplumber.open("output/test_dy_desc.pdf") as pdf:
    words = [w for w in pdf.pages[0].extract_words() if 325 <= w['top'] <= 365 and 120 <= w['x0'] <= 250]
    print("Words in test_dy_desc.pdf:")
    for w in sorted(words, key=lambda x: (x['top'], x['x0'])):
        print(f"  top={w['top']:.2f}, x0={w['x0']:.2f}: {repr(w['text'])}")
