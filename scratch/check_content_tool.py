import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

client = PdfCraftClient()
doc_id = client.doc_open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf")

res = client.call_tool("content_list", {"doc": doc_id})
print("Keys in content_list res:", res.keys())
items = res.get('content', [])
print("Total content items:", len(items))
for item in items[:5]:
    print(" ", item)

client.doc_close(doc_id, discard_changes=True)
