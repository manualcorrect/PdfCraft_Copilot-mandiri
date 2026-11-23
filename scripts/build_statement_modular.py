"""
Modular Bank Mandiri e-Statement Builder
Supports AUG, SEP, OCT with pixel-perfect alignment and standard specifications.
"""

import os
import sys
import shutil
import re
import datetime
import openpyxl
import pdfplumber

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from pdfcraft_client import PdfCraftClient
from bank_mandiri_spec import (
    COL_NOMINAL_RIGHT_X,
    COL_SALDO_RIGHT_X,
    SUMMARY_RIGHT_X,
    COL_NO_X,
    COL_DATE_TIME_X0,
    COL_DESC_X,
    VALUE_COL1_X0,
    VALUE_COL2_X0,
    COLOR_CREDIT_GREEN,
    COLOR_RUNNING_SALDO_BLUE,
    COLOR_DEBIT_BLACK,
    COLOR_SALDO_AWAL_GRAY
)

def format_idr(num):
    return f"{abs(num):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def parse_num(val):
    if val is None:
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    val_str = str(val).replace("Rp", "").replace(" ", "").replace(".", "").replace(",", ".").strip()
    try:
        return float(val_str)
    except:
        return 0.0

def build_statement(month_code: str, excel_path: str, pdf_source: str, output_pdf_path: str, allow_zero_nominals: bool = False):
    print(f"\n{'='*25} BUILDING {month_code} STATEMENT {'='*25}")
    templates_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "templates"))
    p1_template = os.path.join(templates_dir, "master_page_1.pdf")
    p_mid_template = os.path.join(templates_dir, "master_page_intermediate.pdf")
    p_disc_inline = os.path.join(templates_dir, "master_page_disclaimer_inline.pdf")
    p_disc_standalone = os.path.join(templates_dir, "master_page_disclaimer_standalone.pdf")

    # 1. Parse Excel Header & Financial Summary
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    ws1 = wb["Header & Ringkasan"]
    ws2 = wb["Tabel_Mutasi"]

    cabang = str(ws1.cell(11, 2).value or "KCP Serang Ciceri").strip()
    periode = str(ws1.cell(12, 2).value or "").strip()
    dicetak_cell = ws1.cell(13, 2).value
    if isinstance(dicetak_cell, datetime.datetime):
        dicetak_pada = dicetak_cell.strftime("%d %b %Y")
    else:
        dicetak_pada = str(dicetak_cell or "09 Sep 2026").strip()
    nomor_rekening = str(ws1.cell(14, 2).value or "1630016287487").strip()

    header = {
        "nama_line1": "GALANG PUTRA",
        "nama_line2": "KURNIAWAN",
        "cabang": cabang,
        "periode": periode,
        "dicetak_pada": dicetak_pada,
        "nomor_rekening": nomor_rekening
    }

    sawal_val = parse_num(ws1.cell(22, 2).value)
    dmasuk_val = parse_num(ws1.cell(23, 2).value)
    dkeluar_val = abs(parse_num(ws1.cell(24, 2).value))
    sakhir_val = sawal_val + dmasuk_val - dkeluar_val

    summary = {
        "saldo_awal": format_idr(sawal_val),
        "dana_masuk": format_idr(dmasuk_val),
        "dana_keluar": format_idr(dkeluar_val),
        "saldo_akhir": format_idr(sakhir_val)
    }

    print(f"Header: {header}")
    print(f"Summary: {summary}")

    # 2. Harvest authentic items from PDF source
    authentic_items = []
    with pdfplumber.open(pdf_source) as pdf:
        for p_idx, page in enumerate(pdf.pages):
            words = page.extract_words()
            min_top = 320 if p_idx == 0 else 200
            table_words = [w for w in words if min_top <= w["top"] <= 800]
            
            wib_words = sorted([w for w in table_words if w['text'] == 'WIB'], key=lambda x: x['top'])
            for ww in wib_words:
                time_token = [w['text'] for w in table_words if abs(w['top'] - ww['top']) < 3 and w['x1'] <= ww['x0'] + 1]
                date_tokens = [w['text'] for w in table_words if 0 < (ww['top'] - w['top']) < 15 and 45 <= w['x0'] <= 90]
                
                desc_words = sorted([w for w in table_words if abs(w['top'] - ww['top']) < 22 and 115 <= w['x0'] <= 365], key=lambda x: (x['top'], x['x0']))
                lines = []
                curr_l = []
                curr_y = None
                for w in desc_words:
                    if curr_y is None or abs(w['top'] - curr_y) < 4:
                        curr_l.append(w['text'])
                        curr_y = w['top'] if curr_y is None else (curr_y * 0.7 + w['top'] * 0.3)
                    else:
                        lines.append(" ".join(curr_l))
                        curr_l = [w['text']]
                        curr_y = w['top']
                if curr_l:
                    lines.append(" ".join(curr_l))
                desc_text = "\n".join(lines)

                t_str = f"{time_token[-1]} WIB" if time_token else "12:00:00 WIB"
                raw_d = " ".join(date_tokens).strip()
                for m_old in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]:
                    raw_d = raw_d.replace(m_old, month_code.capitalize())
                d_str = re.sub(r'(\d+)\s*([A-Za-z]+)\s*(\d+)', r'\1 \2 \3', raw_d)

                authentic_items.append({
                    "date": d_str,
                    "time": t_str,
                    "desc": desc_text
                })

    print(f"Harvested {len(authentic_items)} authentic items from {pdf_source}")

    # 3. Read active transactions from Excel
    excel_txs = []
    for r in range(6, ws2.max_row + 1):
        nom_cell = ws2.cell(r, 5).value
        sal_cell = ws2.cell(r, 7).value
        if nom_cell is None or str(nom_cell).strip() == '':
            continue
        nom = parse_num(nom_cell)
        sal = parse_num(sal_cell)
        
        if abs(nom) > 0.001 or allow_zero_nominals:
            date_cell = ws2.cell(r, 2).value
            time_cell = ws2.cell(r, 3).value
            
            formatted_date_ex = None
            if date_cell:
                if isinstance(date_cell, datetime.datetime):
                    formatted_date_ex = date_cell.strftime("%d %b %Y")
                elif isinstance(date_cell, str):
                    formatted_date_ex = date_cell.strip()
                    
            formatted_time_ex = None
            if time_cell:
                t_raw = str(time_cell).strip()
                if "WIB" not in t_raw:
                    t_raw = f"{t_raw} WIB"
                formatted_time_ex = t_raw

            excel_txs.append({
                "excel_row": r,
                "nominal_num": nom,
                "saldo_num": sal,
                "date_excel": formatted_date_ex,
                "time_excel": formatted_time_ex
            })

    print(f"Harvested {len(excel_txs)} transactions from Excel")
    total_tx = len(excel_txs)

    # 4. Merge into standardized transactions
    transactions = []
    for i in range(total_tx):
        ex = excel_txs[i]
        nom_val = ex["nominal_num"]
        sal_val = ex["saldo_num"]
        
        auth = authentic_items[i] if i < len(authentic_items) else {"date": f"01 {month_code.capitalize()} 2026", "time": "12:00:00 WIB", "desc": "-"}
        tx_date = ex["date_excel"] if ex["date_excel"] else auth["date"]
        tx_time = ex["time_excel"] if ex["time_excel"] else auth["time"]
        
        is_credit = nom_val > 0
        nom_str = ("+" if is_credit else "-") + format_idr(nom_val)
        sal_str = format_idr(sal_val)
        
        transactions.append({
            "no": str(i + 1),
            "date": tx_date,
            "time": tx_time,
            "desc": auth["desc"],
            "nominal": nom_str,
            "saldo": sal_str,
            "is_credit": is_credit
        })

    # 5. Determine Page Capacities & Template structure
    # Page 1: 10
    # Page 2: 12
    # Page 3: 12
    # If total_tx == 34 -> Page 4 is standalone disclaimer (0 tx)
    # If total_tx > 34 (e.g. 35 or 37) -> Page 4 is inline disclaimer
    if total_tx == 34:
        page_capacities = [10, 12, 12]
        page_paths = [p1_template, p_mid_template, p_mid_template, p_disc_standalone]
        is_last_inline = False
    elif total_tx <= 34 + 7: # up to 41 txs
        p4_count = total_tx - 34
        page_capacities = [10, 12, 12, p4_count]
        page_paths = [p1_template, p_mid_template, p_mid_template, p_disc_inline]
        is_last_inline = True
    else:
        raise ValueError(f"Unsupported transaction count: {total_tx}")

    total_pages = len(page_paths)
    print(f"Assembly: {total_pages} pages, capacities: {page_capacities}, last_inline: {is_last_inline}")

    temp_combined = os.path.join(os.path.dirname(output_pdf_path), f"temp_{month_code}_assembly.pdf")
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)

    with PdfCraftClient() as client:
        client.call_tool("doc_combine", {
            "paths": page_paths,
            "out": temp_combined,
            "open": False
        })

        doc_id = client.doc_open(temp_combined)
        print(f"Editing assembled document (doc_id={doc_id})...")

        # Apply Header across all transaction pages
        num_header_pages = 3 if not is_last_inline else 4
        for p_num in range(1, num_header_pages + 1):
            paras = client.get_paragraphs(doc_id, page=p_num)
            
            # Step A: Empty old Cabang paragraph to prevent collision
            p_cabang = [p for p in paras if ("Taman Aries" in p["text"] or "KCP" in p["text"] or "Ciceri" in p["text"]) and 115 <= p["rect"][1] <= 135 and p["rect"][0] < 200]
            if p_cabang:
                client.edit_text(doc_id, page=p_num, paragraph=p_cabang[0]["paragraph"], text="")

            # Step B: Apply 3-line composite block to Name paragraph
            paras = client.get_paragraphs(doc_id, page=p_num)
            p_name = [p for p in paras if ("ROY DARWIN" in p["text"] or "GALANG" in p["text"]) and 90 <= p["rect"][1] <= 115 and p["rect"][0] < 200]
            if p_name:
                composite_text = f"{header['nama_line1']}\n{header['nama_line2']}\n{header['cabang']}"
                client.edit_text(doc_id, page=p_num, paragraph=p_name[0]["paragraph"], text=composite_text, line_spacing=1.375)
                up_p = [x for x in client.get_paragraphs(doc_id, page=p_num) if x["paragraph"] == p_name[0]["paragraph"]][0]
                dx = VALUE_COL1_X0 - up_p["rect"][0]
                if abs(dx) > 0.05:
                    client.edit_text(doc_id, page=p_num, paragraph=p_name[0]["paragraph"], dx=dx)

            # Step C: Periode
            paras = client.get_paragraphs(doc_id, page=p_num)
            for p in paras:
                if ("01" in p["text"] and any(m in p["text"] for m in ["Jan", "Feb", "Aug", "Sep", "Oct"])) and 90 <= p["rect"][1] <= 115 and 330 <= p["rect"][0] <= 370:
                    client.edit_text(doc_id, page=p_num, paragraph=p["paragraph"], text=header["periode"])
                    break

            # Step D: Dicetak Pada
            paras = client.get_paragraphs(doc_id, page=p_num)
            for p in paras:
                if any(m in p["text"] for m in ["Sep", "Nov"]) and 115 <= p["rect"][1] <= 135 and 330 <= p["rect"][0] <= 370:
                    client.edit_text(doc_id, page=p_num, paragraph=p["paragraph"], text=header["dicetak_pada"])
                    break

            # Step E: Page Numbers (1 dari 4, 1 of 4, etc.)
            paras = client.get_paragraphs(doc_id, page=p_num)
            for p in paras:
                if p["text"].strip().isdigit() and 545 <= p["rect"][0] <= 575 and 90 <= p["rect"][1] <= 110:
                    client.edit_text(doc_id, page=p_num, paragraph=p["paragraph"], text="")

            paras = client.get_paragraphs(doc_id, page=p_num)
            for p in paras:
                if "dari" in p["text"] and 520 <= p["rect"][0] <= 570 and 90 <= p["rect"][1] <= 115:
                    client.edit_text(doc_id, page=p_num, paragraph=p["paragraph"], text=f"{p_num} dari {total_pages}", width=50.0)
                elif "of" in p["text"] and 530 <= p["rect"][0] <= 570 and 105 <= p["rect"][1] <= 125:
                    client.edit_text(doc_id, page=p_num, paragraph=p["paragraph"], text=f"{p_num} of {total_pages}", width=50.0)

        # Page 1 Account Number & Financial Summary
        paras = client.get_paragraphs(doc_id, page=1)
        for p in paras:
            if "1650003584860" in p["text"] or "1660003584860" in p["text"] or "1630016287487" in p["text"]:
                client.edit_text(doc_id, page=1, paragraph=p["paragraph"], text=f"{header['nomor_rekening']} ")
                break

        paras = client.get_paragraphs(doc_id, page=1)
        p_sawal = [p for p in paras if 160 <= p["rect"][1] <= 180 and p["rect"][0] > 480][0]
        client.edit_text(doc_id, page=1, paragraph=p_sawal["paragraph"], text=summary["saldo_awal"], color=COLOR_SALDO_AWAL_GRAY)
        up = [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == p_sawal["paragraph"]][0]
        dx = SUMMARY_RIGHT_X - up["rect"][2]
        if abs(dx) > 0.01: client.edit_text(doc_id, page=1, paragraph=up["paragraph"], dx=dx)

        paras = client.get_paragraphs(doc_id, page=1)
        p_dmasuk = [p for p in paras if 185 <= p["rect"][1] <= 205 and p["rect"][0] > 480][0]
        client.edit_text(doc_id, page=1, paragraph=p_dmasuk["paragraph"], text=f"+ {summary['dana_masuk']}", color=COLOR_CREDIT_GREEN)
        up = [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == p_dmasuk["paragraph"]][0]
        dx = SUMMARY_RIGHT_X - up["rect"][2]
        if abs(dx) > 0.01: client.edit_text(doc_id, page=1, paragraph=up["paragraph"], dx=dx)

        paras = client.get_paragraphs(doc_id, page=1)
        p_dkeluar = [p for p in paras if 208 <= p["rect"][1] <= 228 and p["rect"][0] > 480][0]
        client.edit_text(doc_id, page=1, paragraph=p_dkeluar["paragraph"], text=f"- {summary['dana_keluar']}", color=COLOR_DEBIT_BLACK)
        up = [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == p_dkeluar["paragraph"]][0]
        dx = SUMMARY_RIGHT_X - up["rect"][2]
        if abs(dx) > 0.01: client.edit_text(doc_id, page=1, paragraph=up["paragraph"], dx=dx)

        paras = client.get_paragraphs(doc_id, page=1)
        p_sakhir = [p for p in paras if 230 <= p["rect"][1] <= 255 and p["rect"][0] > 480][0]
        client.edit_text(doc_id, page=1, paragraph=p_sakhir["paragraph"], text=summary["saldo_akhir"], color=COLOR_RUNNING_SALDO_BLUE)
        up = [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == p_sakhir["paragraph"]][0]
        dx = SUMMARY_RIGHT_X - up["rect"][2]
        if abs(dx) > 0.01: client.edit_text(doc_id, page=1, paragraph=up["paragraph"], dx=dx)

        # Populate Transactions Page by Page
        tx_cursor = 0
        for p_idx, num_rows in enumerate(page_capacities):
            p_num = p_idx + 1
            base_y_start = 343.92 if p_num == 1 else 227.92
            max_template_rows = 10 if p_num == 1 else (12 if p_num in [2, 3] else 7)

            for r_i in range(num_rows):
                tx = transactions[tx_cursor]
                tx_cursor += 1
                row_y = base_y_start + r_i * 46.00

                # No Urut
                paras = client.get_paragraphs(doc_id, page=p_num)
                p_no = [p for p in paras if abs(p["rect"][1] - row_y) < 15 and 15 <= p["rect"][0] <= 45]
                if p_no:
                    client.edit_text(doc_id, page=p_num, paragraph=p_no[0]["paragraph"], text=tx["no"])

                # Date
                paras = client.get_paragraphs(doc_id, page=p_num)
                p_date = [p for p in paras if 45 <= p["rect"][0] <= 80 and abs(p["rect"][1] - (row_y - 4.0)) < 4.0]
                if p_date:
                    client.edit_text(doc_id, page=p_num, paragraph=p_date[0]["paragraph"], text=tx["date"])
                else:
                    p_date_fb = [p for p in paras if 45 <= p["rect"][0] <= 80 and abs(p["rect"][1] - row_y) < 15 and "WIB" not in p["text"]]
                    if p_date_fb:
                        client.edit_text(doc_id, page=p_num, paragraph=p_date_fb[0]["paragraph"], text=tx["date"])

                # Time
                paras = client.get_paragraphs(doc_id, page=p_num)
                p_time = [p for p in paras if 45 <= p["rect"][0] <= 80 and abs(p["rect"][1] - (row_y + 5.0)) < 4.0]
                if p_time:
                    client.edit_text(doc_id, page=p_num, paragraph=p_time[0]["paragraph"], text=tx["time"])
                else:
                    p_time_fb = [p for p in paras if 45 <= p["rect"][0] <= 80 and abs(p["rect"][1] - row_y) < 15 and "WIB" in p["text"]]
                    if p_time_fb:
                        client.edit_text(doc_id, page=p_num, paragraph=p_time_fb[0]["paragraph"], text=tx["time"])

                # Description with vertical centering
                paras = client.get_paragraphs(doc_id, page=p_num)
                p_desc = [p for p in paras if abs(p["rect"][1] - row_y) < 20 and 120 <= p["rect"][0] <= 360]
                if p_desc:
                    desc_target_para = p_desc[0]["paragraph"]
                    client.edit_text(doc_id, page=p_num, paragraph=desc_target_para, text=tx["desc"])
                    
                    up_paras = client.get_paragraphs(doc_id, page=p_num)
                    matched_up = [p for p in up_paras if p["paragraph"] == desc_target_para]
                    if matched_up:
                        up_p = matched_up[0]
                        num_lines = len(tx["desc"].split("\n"))
                        target_y = row_y - (num_lines - 1) * 5.0
                        dy = up_p["rect"][1] - target_y
                        if abs(dy) > 0.01:
                            client.edit_text(doc_id, page=p_num, paragraph=desc_target_para, dy=dy)

                # Nominal
                paras = client.get_paragraphs(doc_id, page=p_num)
                p_nom = [p for p in paras if abs(p["rect"][1] - row_y) < 15 and 370 <= p["rect"][0] <= 470]
                if p_nom:
                    col = COLOR_CREDIT_GREEN if tx["is_credit"] else COLOR_DEBIT_BLACK
                    client.edit_text(doc_id, page=p_num, paragraph=p_nom[0]["paragraph"], text=tx["nominal"], color=col)
                    up = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == p_nom[0]["paragraph"]][0]
                    dx = COL_NOMINAL_RIGHT_X - up["rect"][2]
                    if abs(dx) > 0.01: client.edit_text(doc_id, page=p_num, paragraph=up["paragraph"], dx=dx)

                # Saldo
                paras = client.get_paragraphs(doc_id, page=p_num)
                p_sal = [p for p in paras if abs(p["rect"][1] - row_y) < 15 and 490 <= p["rect"][0] <= 585]
                if p_sal:
                    client.edit_text(doc_id, page=p_num, paragraph=p_sal[0]["paragraph"], text=tx["saldo"], color=COLOR_RUNNING_SALDO_BLUE)
                    up = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == p_sal[0]["paragraph"]][0]
                    dx = COL_SALDO_RIGHT_X - up["rect"][2]
                    if abs(dx) > 0.01: client.edit_text(doc_id, page=p_num, paragraph=up["paragraph"], dx=dx)

            # On last inline page: blank out unused rows
            if is_last_inline and p_num == total_pages and num_rows < max_template_rows:
                for unused_r_i in range(num_rows, max_template_rows):
                    unused_y = base_y_start + unused_r_i * 46.00
                    paras = client.get_paragraphs(doc_id, page=p_num)
                    for p in paras:
                        if abs(p["rect"][1] - unused_y) < 20.0 and p["rect"][1] < 580:
                            client.edit_text(doc_id, page=p_num, paragraph=p["paragraph"], text="")

        # Save finalized PDF
        client.doc_save(doc_id, path=output_pdf_path, full=True)
        client.doc_close(doc_id)

    if os.path.exists(temp_combined):
        try: os.remove(temp_combined)
        except: pass

    print(f"\n[DONE] Successfully built statement at: {output_pdf_path}")

if __name__ == "__main__":
    oct_excel = r"output\Template_Mutasi_OCT_Reconciled.xlsx"
    oct_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\1.pdf"
    oct_out = r"output\REK_GALANG_OCT_2026.pdf"
    build_statement("OCT", oct_excel, oct_pdf, oct_out)
