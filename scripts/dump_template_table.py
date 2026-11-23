import sys
import os
sys.path.append(os.path.abspath("src"))
sys.stdout.reconfigure(encoding='utf-8')
from pdfcraft_client import PdfCraftClient

with PdfCraftClient() as client:
    doc_id = client.doc_open("templates/master_page_1.pdf")
    
    # Check all paragraphs on page 1
    paras = client.get_paragraphs(doc_id, page=1)
    table_paras = [p for p in paras if 320 <= p["rect"][1] <= 800]
    print(f"Total table paragraphs: {len(table_paras)}")
    for p in table_paras:
        print(f"  P#{p['paragraph']:2d} rect={p['rect']} text={repr(p['text'])}")
        
    client.doc_close(doc_id, discard_changes=True)
