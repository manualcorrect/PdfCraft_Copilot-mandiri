import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

client = PdfCraftClient()
doc_id = client.doc_open(r'scratch/test_copy.pdf')
res = client.call_tool("text_lines", {"doc": doc_id, "page": 3})
lines = res.get('lines', [])

# find lines near y=730-760 (bottom of page 3)
p3_bottom = [l for l in lines if 720 <= l['rect'][1] <= 780]
for l in p3_bottom:
    print(f"Line {l['line']} rect={l['rect']} text='{l['text']}' font='{l['font']}'")

client.doc_close(doc_id, discard_changes=True)
