import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

client = PdfCraftClient()
doc_id = client.doc_open(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf')

for p in range(2, 6):
    paras = client.get_paragraphs(doc_id, page=p)
    print(f"=== PAGE {p} (y < 200) ===")
    for para in paras:
        r = [round(x, 1) for x in para['rect']]
        if r[1] < 200:
            print(f"P{para['paragraph']:2d} rect={r} text='{para.get('text', '')}'")

client.doc_close(doc_id, discard_changes=True)
