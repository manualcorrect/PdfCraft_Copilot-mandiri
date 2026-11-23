import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from pdfcraft_client import PdfCraftClient
import pdfplumber

with PdfCraftClient() as client:
    doc_id = client.doc_open('templates/master_page_1.pdf')
    # Empty cabang paragraph 22
    client.edit_text(doc_id, page=1, paragraph=22, text="")
    
    # Set 3 lines on paragraph 21
    composite_text = "GALANG PUTRA\nKURNIAWAN\nKCP Serang Ciceri"
    client.edit_text(doc_id, page=1, paragraph=21, text=composite_text, line_spacing=1.375)
    
    # Check paragraphs & lines
    lines = client.call_tool("text_lines", {"doc": doc_id, "page": 1}).get("lines", [])
    print("=== text_lines in PdfCraft ===")
    for l in lines:
        if l["rect"][1] < 140 and l["rect"][0] < 300:
            print(f"  {l['rect']}: {repr(l['text'])}")
            
    client.doc_save(doc_id, path='output/test_name_render.pdf')
    client.doc_close(doc_id)

print("\n=== pdfplumber extraction ===")
with pdfplumber.open('output/test_name_render.pdf') as pdf:
    words = pdf.pages[0].extract_words()
    for w in sorted([w for w in words if w['top'] < 140 and w['x0'] < 300], key=lambda x: (x['top'], x['x0'])):
        print(f"  top={w['top']:.2f}, bottom={w['bottom']:.2f}, x0={w['x0']:.2f}, text={repr(w['text'])}")
