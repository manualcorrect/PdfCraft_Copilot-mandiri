import sys
import os
sys.path.append(os.path.abspath("src"))
sys.stdout.reconfigure(encoding='utf-8')
from pdfcraft_client import PdfCraftClient

galang_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\REK GALANG JUL 2026.pdf"

with PdfCraftClient() as client:
    doc_id = client.doc_open(galang_path)
    res = client.call_tool("text_lines", {"doc": doc_id, "page": 1})
    print("Text lines in authentic Galang page 1:")
    for line in res.get("lines", []):
        if line["rect"][1] < 140 and line["rect"][0] < 220:
            print(f"  Line rect={line['rect']} text={repr(line['text'])}")
    client.doc_close(doc_id, discard_changes=True)
