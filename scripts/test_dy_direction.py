import sys
import os
sys.path.append(os.path.abspath("src"))
sys.stdout.reconfigure(encoding='utf-8')
from pdfcraft_client import PdfCraftClient

with PdfCraftClient() as client:
    doc_id = client.doc_open("templates/master_page_1.pdf")
    
    print("Testing dy=+10.00 on P85:")
    client.edit_text(doc_id, 1, 85, text="Biaya administrasi kartu debit", dy=10.00)
    
    paras = client.get_paragraphs(doc_id, 1)
    p85 = next(p for p in paras if "Biaya" in p["text"])
    print(f"P85 after dy=+10.00: rect={p85['rect']}")
    
    print("\nTesting dy=-10.00 on P85:")
    client.edit_text(doc_id, 1, p85["paragraph"], dy=-10.00)
    paras = client.get_paragraphs(doc_id, 1)
    p85 = next(p for p in paras if "Biaya" in p["text"])
    print(f"P85 after dy=-10.00: rect={p85['rect']}")
    
    client.doc_close(doc_id, discard_changes=True)
