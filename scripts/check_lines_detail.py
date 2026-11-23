import sys
import os
sys.path.append(os.path.abspath("src"))
sys.stdout.reconfigure(encoding='utf-8')
from pdfcraft_client import PdfCraftClient

with PdfCraftClient() as client:
    doc_id = client.doc_open("output/REK_GALANG_JUL_2026_STANDARDIZED.pdf")
    lines = client.call_tool("text_lines", {"doc": doc_id, "page": 1}).get("lines", [])
    print("Page 1 lines between Y 640 and 740:")
    for l in lines:
        if 640 <= l["rect"][1] <= 740 and 120 <= l["rect"][0] <= 360:
            print(f"  Y={l['rect'][1]:.2f}-{l['rect'][3]:.2f}, X={l['rect'][0]:.2f}-{l['rect'][2]:.2f}: {repr(l['text'])}")
    client.doc_close(doc_id, discard_changes=True)
