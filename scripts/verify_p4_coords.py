import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from pdfcraft_client import PdfCraftClient

with PdfCraftClient() as client:
    t_name = 'master_page_disclaimer_inline.pdf'
    path = os.path.join('templates', t_name)
    doc_id = client.doc_open(path)
    paras = client.get_paragraphs(doc_id, page=1)
    print(f"=== {t_name} ===")
    base_y_start = 227.92
    for r_i in range(3):
        row_y = base_y_start + r_i * 46.00
        d_p = [p for p in paras if 45 <= p['rect'][0] <= 80 and abs(p['rect'][1] - (row_y - 4.0)) < 3.0]
        t_p = [p for p in paras if 45 <= p['rect'][0] <= 80 and abs(p['rect'][1] - (row_y + 5.0)) < 3.0]
        d_text = d_p[0]['text'] if d_p else "NOT FOUND"
        t_text = t_p[0]['text'] if t_p else "NOT FOUND"
        d_para = d_p[0]['paragraph'] if d_p else "-"
        t_para = t_p[0]['paragraph'] if t_p else "-"
        print(f"  Row {r_i+1:02d} (row_y={row_y:.2f}): Date [P{d_para}]: {repr(d_text):15} | Time [P{t_para}]: {repr(t_text)}")
    client.doc_close(doc_id)
