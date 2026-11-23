import sys
import os
sys.path.append(os.path.abspath("src"))
sys.stdout.reconfigure(encoding='utf-8')
from pdfcraft_client import PdfCraftClient

with PdfCraftClient() as client:
    doc_id = client.doc_open("templates/master_page_1.pdf")
    
    print("Editing P#43 to 2 lines:")
    client.edit_text(doc_id, page=1, paragraph=43, text="Pembayaran Danatopup\n89508089528734111", width=240.0)
    
    paras = client.get_paragraphs(doc_id, page=1)
    p_row1 = [p for p in paras if 330 <= p["rect"][1] <= 370]
    print(f"Row 1 paragraphs after edit ({len(p_row1)}):")
    for p in p_row1:
        print(f"  P#{p['paragraph']:2d} rect={p['rect']} text={repr(p['text'])}")
        
    p_row2 = [p for p in paras if 370 <= p["rect"][1] <= 420]
    print(f"Row 2 paragraphs after edit ({len(p_row2)}):")
    for p in p_row2:
        print(f"  P#{p['paragraph']:2d} rect={p['rect']} text={repr(p['text'])}")
        
    client.doc_close(doc_id, discard_changes=True)
