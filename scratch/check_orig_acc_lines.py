import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

client = PdfCraftClient()
doc_id = client.doc_open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf")

res = client.call_tool("text_lines", {"doc": doc_id, "page": 1})
lines = res.get('lines', [])
for l in lines:
    if '1650003584860' in l.get('text', '') or (185 <= l['rect'][1] <= 195 and l['rect'][0] < 250):
        print("Line:", l)

client.doc_close(doc_id, discard_changes=True)
