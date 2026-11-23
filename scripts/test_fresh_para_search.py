import sys
import os
sys.path.append(os.path.abspath("src"))
sys.stdout.reconfigure(encoding='utf-8')
from pdfcraft_client import PdfCraftClient

def find_para(client, doc_id, page, x_range, y_range, predicate=None):
    paras = client.get_paragraphs(doc_id, page=page)
    for p in paras:
        r = p["rect"]
        if x_range[0] <= r[0] <= x_range[1] and y_range[0] <= r[1] <= y_range[1]:
            if predicate is None or predicate(p):
                return p
    return None

with PdfCraftClient() as client:
    doc_id = client.doc_open("templates/master_page_1.pdf")
    
    # 1. Clear Cabang
    p_cabang = find_para(client, doc_id, page=1, x_range=(115, 135), y_range=(118, 132))
    print(f"Found Cabang: P#{p_cabang['paragraph']} {p_cabang['text']}")
    client.edit_text(doc_id, page=1, paragraph=p_cabang["paragraph"], text="")
    
    # 2. Set Name + Cabang
    p_name = find_para(client, doc_id, page=1, x_range=(115, 135), y_range=(95, 110))
    print(f"Found Name: P#{p_name['paragraph']} {p_name['text']}")
    client.edit_text(doc_id, page=1, paragraph=p_name["paragraph"], 
                     text="GALANG PUTRA\nKURNIAWAN\nKCP Serang Ciruas", 
                     line_spacing=1.375)
    
    # 3. Periode
    p_periode = find_para(client, doc_id, page=1, x_range=(330, 370), y_range=(95, 110))
    print(f"Found Periode: P#{p_periode['paragraph']} {p_periode['text']}")
    client.edit_text(doc_id, page=1, paragraph=p_periode["paragraph"], text="01 Jul 2026 - 31 Jul 2026")
    
    # 4. Dicetak pada
    p_dicetak = find_para(client, doc_id, page=1, x_range=(330, 370), y_range=(118, 132))
    print(f"Found Dicetak: P#{p_dicetak['paragraph']} {p_dicetak['text']}")
    client.edit_text(doc_id, page=1, paragraph=p_dicetak["paragraph"], text="19 Oct 2026")
    
    lines = client.call_tool("text_lines", {"doc": doc_id, "page": 1}).get("lines", [])
    print("\nResulting Lines in Header:")
    for l in lines:
        if l["rect"][1] < 140:
            print(f"  {l['rect']}: {repr(l['text'])}")
            
    client.doc_close(doc_id, discard_changes=True)
