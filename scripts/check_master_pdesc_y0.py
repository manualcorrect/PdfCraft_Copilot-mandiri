import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from pdfcraft_client import PdfCraftClient

with PdfCraftClient() as client:
    doc_id = client.doc_open("templates/master_page_1.pdf")
    paras = client.get_paragraphs(doc_id, page=1)
    for r in range(1, 11):
        row_y = 343.92 + (r - 1) * 46.00
        p_desc = [p for p in paras if abs(p["rect"][1] - row_y) < 20 and 120 <= p["rect"][0] <= 135]
        if p_desc:
            print(f"Row {r:02d} (row_y={row_y:.2f}): P{p_desc[0]['paragraph']} y0={p_desc[0]['rect'][1]:.2f}, text={repr(p_desc[0]['text'])[:40]}")
    client.doc_close(doc_id)
