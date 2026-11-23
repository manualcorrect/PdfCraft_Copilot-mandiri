import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

client = PdfCraftClient()
doc_id = client.doc_open(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf')

paras = client.get_paragraphs(doc_id, page=1)
print(f"=== ALL PARAS ON PAGE 1 (y < 300) ===")
for p in paras:
    r = [round(x, 1) for x in p['rect']]
    if r[1] < 300:
        print(f"P{p['paragraph']:2d} rect={r} text='{p.get('text', '')}'")

client.doc_close(doc_id, discard_changes=True)
