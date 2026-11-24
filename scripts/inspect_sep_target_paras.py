import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

with PdfCraftClient() as client:
    doc_id = client.doc_open(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\sep\0.pdf')
    
    print("=== TX 10 (Page 1) ===")
    p1_paras = client.get_paragraphs(doc_id, page=1)
    for p in p1_paras:
        if p['rect'][1] > 730:
            print(f"Para {p['paragraph']:2d} [rect={p['rect']}]: {repr(p['text'])}")
            
    print("\n=== TX 33 (Page 3) ===")
    p3_paras = client.get_paragraphs(doc_id, page=3)
    for p in p3_paras:
        if 670 <= p['rect'][1] <= 720:
            print(f"Para {p['paragraph']:2d} [rect={p['rect']}]: {repr(p['text'])}")

    print("\n=== TX 46 (Page 4) ===")
    p4_paras = client.get_paragraphs(doc_id, page=4)
    for p in p4_paras:
        if p['rect'][1] >= 720:
            print(f"Para {p['paragraph']:2d} [rect={p['rect']}]: {repr(p['text'])}")

    client.doc_close(doc_id)
