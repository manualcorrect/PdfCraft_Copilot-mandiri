import sys
import os
sys.path.append(os.path.abspath("src"))
sys.stdout.reconfigure(encoding='utf-8')
from pdfcraft_client import PdfCraftClient

with PdfCraftClient() as client:
    doc_id = client.doc_open("templates/master_page_1.pdf")
    print("Initial paragraphs:")
    for p in client.get_paragraphs(doc_id, page=1):
        if p["rect"][1] < 150:
            print(f"P#{p['paragraph']:2d} rect={p['rect']} text={repr(p['text'])}")
            
    print("\nEditing P#21 (Name) to 2 lines...")
    client.edit_text(doc_id, page=1, paragraph=21, text="GALANG PUTRA\nKURNIAWAN", line_spacing=0.85, width=120.0)
    
    print("\nParagraphs AFTER editing P#21:")
    for p in client.get_paragraphs(doc_id, page=1):
        if p["rect"][1] < 150:
            print(f"P#{p['paragraph']:2d} rect={p['rect']} text={repr(p['text'])}")
            
    client.doc_close(doc_id)
