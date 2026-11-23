import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

client = PdfCraftClient()
doc_id = client.doc_open(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf')

for p in [1, 2]:
    paras = client.get_paragraphs(doc_id, page=p)
    print(f"=== PAGE {p} TRANSACTIONS ===")
    min_y = 315 if p == 1 else 200
    tx_paras = [x for x in paras if x['rect'][1] >= min_y]
    # sort by y0
    tx_paras.sort(key=lambda x: (round(x['rect'][1], 1), round(x['rect'][0], 1)))
    for para in tx_paras:
        r = [round(x, 1) for x in para['rect']]
        print(f"P{para['paragraph']:2d} rect={r} text='{para.get('text', '')}'")

client.doc_close(doc_id, discard_changes=True)
