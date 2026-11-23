import sys
import os
sys.path.append(os.path.abspath("src"))
sys.stdout.reconfigure(encoding='utf-8')
from pdfcraft_client import PdfCraftClient

with PdfCraftClient() as client:
    doc_id = client.doc_open("templates/master_page_1.pdf")
    
    paras = client.get_paragraphs(doc_id, 1)
    p85 = next(p for p in paras if p["paragraph"] == 85)
    print(f"P85 before: rect={p85['rect']} text={p85['text']}")
    
    desc_val = "Pembayaran QR\nke kantin wak kaji\n507029124072"
    client.edit_text(doc_id, 1, 85, text=desc_val, width=240.0, dy=-10.00)
    
    lines = client.call_tool("text_lines", {"doc": doc_id, "page": 1}).get("lines", [])
    print("Lines for P85 after edit with dy=-10.00:")
    for l in lines:
        if 640 <= l["rect"][1] <= 720 and 120 <= l["rect"][0] <= 300:
            print(f"  {l['rect']}: {repr(l['text'])}")
            
    client.doc_close(doc_id, discard_changes=True)
