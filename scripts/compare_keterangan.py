import sys
sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient
import pdfplumber

aug_edited = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\REK_GALANG_AUG_2026_edited ketengangan.pdf"
ref_2 = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\2.pdf"

print("--- COMPARING PARAGRAPHS IN EDITED vs REF 2 ---")
with PdfCraftClient() as client:
    doc_ed = client.doc_open(aug_edited)
    doc_ref = client.doc_open(ref_2)
    
    for p in range(1, 5):
        print(f"\n================ PAGE {p} ================")
        paras_ed = client.get_paragraphs(doc_ed, page=p)
        paras_ref = client.get_paragraphs(doc_ref, page=p)
        print(f"Total paras - Edited: {len(paras_ed)}, Ref: {len(paras_ref)}")
        
        # Look at keterangan paragraphs (x0 between 90 and 380, y between 200 and 800)
        # Exclude headers/disclaimers
        ket_ed = [x for x in paras_ed if 85 <= x["rect"][0] <= 150 and 200 <= x["rect"][1] <= 780]
        ket_ref = [x for x in paras_ref if 85 <= x["rect"][0] <= 150 and 200 <= x["rect"][1] <= 780]
        
        print(f"Keterangan paras count - Edited: {len(ket_ed)}, Ref: {len(ket_ref)}")
        for i in range(min(len(ket_ed), len(ket_ref))):
            ed = ket_ed[i]
            rf = ket_ref[i]
            print(f"Row {i+1}:")
            print(f"  REF : rect={rf['rect']}, font={rf.get('font')}, size={rf.get('size')}")
            print(f"        text={repr(rf['text'][:45])}")
            print(f"  EDIT: rect={ed['rect']}, font={ed.get('font')}, size={ed.get('size')}")
            print(f"        text={repr(ed['text'][:45])}")
            if ed['rect'] != rf['rect'] or ed['text'] != rf['text']:
                print(f"        DIFF! text_changed={ed['text'] != rf['text']}, rect_diff={[round(ed['rect'][j]-rf['rect'][j], 2) for j in range(4)]}")

    client.doc_close(doc_ed)
    client.doc_close(doc_ref)
