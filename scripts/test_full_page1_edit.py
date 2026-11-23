import sys
import os
sys.path.append(os.path.abspath("src"))
sys.stdout.reconfigure(encoding='utf-8')
from pdfcraft_client import PdfCraftClient
from description_layout_engine import DescriptionLayoutEngine, DESC_COL_MAX_WIDTH
from parse_excel_template import parse_xara_excel_template
from bank_mandiri_spec import (
    COL_NOMINAL_RIGHT_X, COL_SALDO_RIGHT_X, COL_NO_X, 
    COL_DATE_TIME_X0, COL_DESC_X, COLOR_CREDIT_GREEN, COLOR_DEBIT_BLACK, COLOR_RUNNING_SALDO_BLUE
)

data = parse_xara_excel_template("templates/Galang_Jul_2026.xlsx")
txs = data["transactions"][:10]

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
    
    base_y_start = 343.92
    for r_i, tx in enumerate(txs):
        row_y = base_y_start + r_i * 46.00
        
        # 1. No
        p_no = find_para(client, doc_id, 1, (15, 35), (row_y - 15, row_y + 15), lambda p: p["text"].strip().isdigit())
        if p_no:
            client.edit_text(doc_id, 1, p_no["paragraph"], text=str(tx["no"]))
            
        # 2. Tanggal
        p_date = find_para(client, doc_id, 1, (45, 75), (row_y - 15, row_y + 5))
        if p_date:
            date_val = tx.get("tanggal_full", tx.get("tanggal", ""))
            client.edit_text(doc_id, 1, p_date["paragraph"], text=date_val)
            
        # 3. Jam
        p_time = find_para(client, doc_id, 1, (45, 75), (row_y + 2, row_y + 20))
        if p_time:
            client.edit_text(doc_id, 1, p_time["paragraph"], text=tx["jam"])
            
        # 4. Keterangan
        p_desc = find_para(client, doc_id, 1, (120, 135), (row_y - 20, row_y + 20))
        if p_desc:
            desc_val = DescriptionLayoutEngine.format_description(tx["uraian"])
            line_count = len(desc_val.split("\n"))
            if line_count == 1:
                target_top_y = row_y
            elif line_count == 2:
                target_top_y = row_y - 5.00
            else:
                target_top_y = row_y - 10.00
            # In PDF space, moving UP requires POSITIVE dy: dy_pdf = current_top_y - target_top_y
            dy = p_desc["rect"][1] - target_top_y
            client.edit_text(doc_id, 1, p_desc["paragraph"], text=desc_val, width=DESC_COL_MAX_WIDTH, dy=dy if abs(dy) >= 0.5 else None)
            
        # 5. Nominal
        p_nom = find_para(client, doc_id, 1, (370, 450), (row_y - 15, row_y + 15))
        if p_nom:
            nom_val = tx["nominal"]
            is_credit = tx["tipe"] == "CR" or nom_val.startswith("+")
            color = COLOR_CREDIT_GREEN if is_credit else COLOR_DEBIT_BLACK
            client.edit_text(doc_id, 1, p_nom["paragraph"], text=nom_val, color=color)
            up_p = next((x for x in client.get_paragraphs(doc_id, 1) if x["paragraph"] == p_nom["paragraph"]), None)
            if up_p:
                dx = COL_NOMINAL_RIGHT_X - up_p["rect"][2]
                if abs(dx) > 0.01:
                    client.edit_text(doc_id, 1, p_nom["paragraph"], dx=dx)
                    
        # 6. Saldo
        p_sal = find_para(client, doc_id, 1, (490, 585), (row_y - 15, row_y + 15))
        if p_sal:
            client.edit_text(doc_id, 1, p_sal["paragraph"], text=tx["saldo"], color=COLOR_RUNNING_SALDO_BLUE)
            up_p = next((x for x in client.get_paragraphs(doc_id, 1) if x["paragraph"] == p_sal["paragraph"]), None)
            if up_p:
                dx = COL_SALDO_RIGHT_X - up_p["rect"][2]
                if abs(dx) > 0.01:
                    client.edit_text(doc_id, 1, p_sal["paragraph"], dx=dx)

    # Let's inspect resulting lines for all rows
    lines = client.call_tool("text_lines", {"doc": doc_id, "page": 1}).get("lines", [])
    print("\nResulting rows on Page 1:")
    for r_i in range(10):
        row_y = base_y_start + r_i * 46.00
        row_lines = [l for l in lines if abs(l["rect"][1] - row_y) < 22.0]
        desc_l = [l for l in row_lines if 120 <= l["rect"][0] <= 135]
        nom_l = [l for l in row_lines if 370 <= l["rect"][0] <= 450]
        sal_l = [l for l in row_lines if 500 <= l["rect"][0] <= 585]
        desc_strs = " / ".join([l["text"] for l in desc_l])
        nom_str = nom_l[0]["text"] if nom_l else "?"
        nom_x1 = nom_l[0]["rect"][2] if nom_l else 0
        sal_str = sal_l[0]["text"] if sal_l else "?"
        sal_x1 = sal_l[0]["rect"][2] if sal_l else 0
        print(f"Row {r_i+1:2d} (Y={row_y:.1f}): Nom={nom_str:13s} (x1={nom_x1:.2f}) | Sal={sal_str:12s} (x1={sal_x1:.2f}) | Desc: {desc_strs}")

    client.doc_close(doc_id, discard_changes=True)
