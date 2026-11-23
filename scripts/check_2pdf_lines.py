import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from pdfcraft_client import PdfCraftClient

with PdfCraftClient() as client:
    doc_id = client.doc_open(r"output\test_edit_2pdf.pdf")
    res = client.call_tool("text_lines", {"doc": doc_id, "page": 1})
    lines = res.get("lines", [])
    print("Page 1 lines count:", len(lines))
    for l in lines[30:55]:
        print(f"  y0={l['rect'][1]:.1f}, x0={l['rect'][0]:.1f}, x1={l['rect'][2]:.1f}: {repr(l['text'])}")
    client.doc_close(doc_id)
