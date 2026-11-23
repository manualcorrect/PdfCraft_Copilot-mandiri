import sys
sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient

aug_edited = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\REK_GALANG_AUG_2026_edited ketengangan.pdf"

with PdfCraftClient() as client:
    doc = client.doc_open(aug_edited)
    for p_num in range(1, 5):
        paras = client.get_paragraphs(doc, page=p_num)
        print(f"\n================ PAGE {p_num} ================")
        min_y = 320 if p_num == 1 else 200
        tbl_paras = [p for p in paras if min_y <= p["rect"][1] <= 800 and 110 <= p["rect"][0] <= 370]
        tbl_paras.sort(key=lambda x: x["rect"][1])
        for p in tbl_paras:
            ed_txt = p.get("editor_text", p["text"])
            print(f"P{p['paragraph']:2d} y={p['rect'][1]:.1f}-{p['rect'][3]:.1f} x={p['rect'][0]:.1f}-{p['rect'][2]:.1f}:")
            for line in ed_txt.split("\n"):
                print(f"     | {line}")
    client.doc_close(doc)
