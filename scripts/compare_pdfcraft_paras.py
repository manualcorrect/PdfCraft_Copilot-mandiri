import sys
import os
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

aug_dir = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug"
p_orig = os.path.join(aug_dir, "0.pdf")
p_out = os.path.join(aug_dir, "REK_KEISYA_AUG_OUTPUT_1.pdf")

with PdfCraftClient() as client:
    d1 = client.doc_open(p_orig)
    paras_orig = client.get_paragraphs(d1, page=1)
    client.doc_close(d1)
    
    d2 = client.doc_open(p_out)
    paras_out = client.get_paragraphs(d2, page=1)
    client.doc_close(d2)

print("--- ORIG PARAGRAPHS (160..260 pt) ---")
for p in paras_orig:
    if 160 <= p["rect"][1] <= 260 and p["rect"][0] > 280:
        print(f"  Para {p['paragraph']:02d} rect={p['rect']}: text='{p['text']}'")

print("\n--- OUT PARAGRAPHS (160..260 pt) ---")
for p in paras_out:
    if 160 <= p["rect"][1] <= 260 and p["rect"][0] > 280:
        print(f"  Para {p['paragraph']:02d} rect={p['rect']}: text='{p['text']}'")
