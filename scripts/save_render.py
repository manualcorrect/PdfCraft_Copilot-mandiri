import sys
sys.path.insert(0, "src")
import base64
from pdfcraft_client import PdfCraftClient

with PdfCraftClient() as client:
    doc = client.doc_open("output/test_oct_clean.pdf")
    res = client.call_tool("page_render", {"doc": doc, "page": 1, "dpi": 150})
    b64_data = res["content"][0]["data"]
    with open("output/test_oct_rendered.png", "wb") as f:
        f.write(base64.b64decode(b64_data))
    client.doc_close(doc)
print("Saved rendered page 1 to output/test_oct_rendered.png")
