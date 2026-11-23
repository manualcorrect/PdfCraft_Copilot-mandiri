import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

client = PdfCraftClient()
doc_id = client.doc_open(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf')
res = client.call_tool("text_lines", {"doc": doc_id, "page": 1})
lines = res.get('lines', [])
for l in lines:
    if l['line'] in [60, 61, 62, 63, 64]:
        print(f"Line {l['line']}: rect={l['rect']} text='{l.get('text')}' font='{l.get('font')}'")
client.doc_close(doc_id, discard_changes=True)
