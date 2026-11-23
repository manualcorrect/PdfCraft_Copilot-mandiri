import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

client = PdfCraftClient()
doc_id = client.doc_open(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf')

for p in range(1, 6):
    paras = client.get_paragraphs(doc_id, page=p)
    print(f"=== PAGE {p} (Total {len(paras)} paras) ===")
    for para in paras:
        txt = para.get('text', '').strip()
        r = [round(x, 1) for x in para['rect']]
        pid = para['paragraph']
        if any(term in txt for term in ['ROY', 'DARWIN', '01Mar', '1 dari', '2 dari', '3 dari', '4 dari', '5 dari', '09Sep', 'Aries', '165000', '16.827', '18.273', '52.488']):
            print(f"  [HDR] P{pid} rect={r}: {txt}")

client.doc_close(doc_id, discard_changes=True)
