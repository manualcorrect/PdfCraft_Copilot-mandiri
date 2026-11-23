import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

client = PdfCraftClient()
doc_id = client.doc_open(r'scratch/test_copy.pdf')

res = client.call_tool("text_lines", {"doc": doc_id, "page": 1})
lines = res.get('lines', [])
sal_lines = [l for l in lines if 565 <= l['rect'][2] <= 575 and l['rect'][1] >= 320]
print("Found Saldo lines on Page 1:", len(sal_lines))
for s in sal_lines:
    print(f"Line {s['line']} rect={s['rect']} text='{s['text']}'")

client.doc_close(doc_id, discard_changes=True)
