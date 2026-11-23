import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from pdfcraft_client import PdfCraftClient

with PdfCraftClient() as client:
    for t_name in ["master_page_intermediate.pdf", "master_page_disclaimer_inline.pdf"]:
        doc_id = client.doc_open(os.path.join("templates", t_name))
        paras = client.get_paragraphs(doc_id, page=1)
        print(f"=== {t_name} Descriptions ===")
        max_r = 12 if "intermediate" in t_name else 3
        for r in range(max_r):
            row_y = 227.92 + r * 46.00
            p_desc = [p for p in paras if abs(p["rect"][1] - row_y) < 20 and 120 <= p["rect"][0] <= 135]
            if p_desc:
                print(f"  Row {r+1:02d} (row_y={row_y:.2f}): P{p_desc[0]['paragraph']} y0={p_desc[0]['rect'][1]:.2f}, text={repr(p_desc[0]['text'])[:35]}")
        client.doc_close(doc_id)
