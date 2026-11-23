import sys
sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient

aug_edited = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\REK_GALANG_AUG_2026_edited ketengangan.pdf"

with PdfCraftClient() as client:
    doc = client.doc_open(aug_edited)
    for p_num in range(1, 5):
        paras = client.get_paragraphs(doc, page=p_num)
        print(f"\n================ PAGE {p_num} ================")
        # Filter paragraphs in table area
        min_y = 320 if p_num == 1 else 200
        tbl_paras = [p for p in paras if min_y <= p["rect"][1] <= 800]
        # sort by y
        tbl_paras.sort(key=lambda x: (x["rect"][1], x["rect"][0]))
        for p in tbl_paras:
            # Let's see all paragraphs
            print(f"P{p['paragraph']:3d} | rect={[round(v, 1) for v in p['rect']]} | font={p.get('font', '')[:15]} | {repr(p['text'])}")
    client.doc_close(doc)
