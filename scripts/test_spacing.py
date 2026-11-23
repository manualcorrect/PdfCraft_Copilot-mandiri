import sys
import os
sys.path.append(os.path.abspath("src"))
sys.stdout.reconfigure(encoding='utf-8')
from pdfcraft_client import PdfCraftClient

with PdfCraftClient() as client:
    doc_id = client.doc_open("templates/master_page_1.pdf")
    client.edit_text(doc_id, page=1, paragraph=22, text="")
    client.edit_text(doc_id, page=1, paragraph=21, text="GALANG PUTRA\nKURNIAWAN\nKCP Serang Ciruas", line_spacing=1.375)
    
    lines_after = client.call_tool("text_lines", {"doc": doc_id, "page": 1}).get("lines", [])
    print("Lines with line_spacing=1.375:")
    for l in lines_after:
        if l["rect"][1] < 140 and 120 <= l["rect"][0] <= 220:
            print(f"  {l['rect']}: {repr(l['text'])}")
            
    client.doc_close(doc_id, discard_changes=True)
