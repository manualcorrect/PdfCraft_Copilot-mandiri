import sys
import os
sys.path.append(os.path.abspath("src"))
sys.stdout.reconfigure(encoding='utf-8')
from pdfcraft_client import PdfCraftClient
from description_layout_engine import DescriptionLayoutEngine, DESC_COL_MAX_WIDTH
from bank_mandiri_spec import COL_DESC_X

with PdfCraftClient() as client:
    doc_id = client.doc_open("templates/master_page_1.pdf")
    
    # Check what happens as we edit row by row
    for r_i in range(10):
        paras = client.get_paragraphs(doc_id, page=1)
        # find desc para for row r_i
        target_y = 343.92 + r_i * 46.00
        desc_candidates = [p for p in paras if 120 <= p["rect"][0] <= 135 and abs(p["rect"][1] - target_y) < 25.0]
        print(f"Row {r_i+1} (target Y={target_y:.2f}) found {len(desc_candidates)} desc candidates:")
        for dc in desc_candidates:
            print(f"   P#{dc['paragraph']} rect={dc['rect']} text={repr(dc['text'][:30])}")
            
    client.doc_close(doc_id, discard_changes=True)
