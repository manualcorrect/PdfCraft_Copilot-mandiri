import sys
import os
sys.path.append(os.path.abspath("src"))
sys.stdout.reconfigure(encoding='utf-8')
from pdfcraft_client import PdfCraftClient

with PdfCraftClient() as client:
    doc_id = client.doc_open("templates/master_page_1.pdf")
    
    # P85 is Row 8 Keterangan at Y=665.92
    paras = client.get_paragraphs(doc_id, 1)
    p85 = next(p for p in paras if p["paragraph"] == 85)
    print(f"P85 before: rect={p85['rect']}")
    
    # We want 3-line description centered: top at 655.92
    # Current screen Y = 665.92. Target screen Y = 655.92.
    # To move UP towards page top, dy_pdf = current_screen_y - target_screen_y = +10.00!
    dy_pdf = p85["rect"][1] - 655.92 # = +10.00
    
    desc_val = "Pembayaran QR\nke kantin wak kaji\n507029124072"
    client.edit_text(doc_id, 1, 85, text=desc_val, width=240.0, dy=dy_pdf)
    
    lines = client.call_tool("text_lines", {"doc": doc_id, "page": 1}).get("lines", [])
    print(f"Lines for P85 after edit with dy_pdf={dy_pdf}:")
    for l in lines:
        if 640 <= l["rect"][1] <= 720 and 120 <= l["rect"][0] <= 300:
            print(f"  {l['rect']}: {repr(l['text'])}")
            
    client.doc_close(doc_id, discard_changes=True)
