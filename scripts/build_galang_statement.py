"""
Build Galang Putra Kurniawan Aug 2026 Standardized e-Statement
Uses authentic Bank Mandiri master templates to construct a pixel-perfect 4-page statement.
Features:
- Composite 3-line header block (2 lines for customer name + 1 line for branch).
- Strict vertical coordinate targeting for Date (row_y - 4.0 pt) and Time (row_y + 5.0 pt).
- Reads custom Date & Time from Excel if specified (e.g. Row 29 / Gaji -> 25 Aug 2026, 04:00:00 WIB).
- Vertical centering & exact 10 pt line spacing for multi-line Keterangan (target_y = row_y - (num_lines - 1) * 5.0, dy = current_y - target_y).
- 100% authentic descriptions from 2.pdf.
- Clean 1..37 sequential numbering and '1 dari 4' / '1 of 4' page numbering.
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

def build_galang_aug_statement(excel_path: str, output_pdf_path: str):
    templates_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "templates"))
    p1_template = os.path.join(templates_dir, "master_page_1.pdf")
    p_mid_template = os.path.join(templates_dir, "master_page_intermediate.pdf")
    p_disc_inline = os.path.join(templates_dir, "master_page_disclaimer_inline.pdf")

    # 1. Parse Excel Header & Financial Summary
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    ws1 = wb["Header & Ringkasan"]
    ws2 = wb["Tabel_Mutasi"]

    cabang = str(ws1.cell(11, 2).value or "KCP Serang Ciceri").strip()
    periode = str(ws1.cell(12, 2).value or "01 Aug 2026 - 31 Aug 2026").strip()
    dicetak_pada = str(ws1.cell(13, 2).value or "09 Sep 2026").strip()
    nomor_rekening = str(ws1.cell(14, 2).value or "1630016287487").strip()

    header = {
        "nama_line1": "GALANG PUTRA",
        "nama_line2": "KURNIAWAN",
        "cabang": cabang,
        "periode": periode,
        "dicetak_pada": dicetak_pada,
        "nomor_rekening": nomor_rekening
    }

    # Financial Summary
    sawal_val = parse_num(ws1.cell(22, 2).value or 4530335.81)
    dmasuk_val = parse_num(ws1.cell(23, 2).value or 7649000.0)
    dkeluar_val = abs(parse_num(ws1.cell(24, 2).value or 7651988.0))
    sakhir_val = sawal_val + dmasuk_val - dkeluar_val

    summary = {
        "saldo_awal": format_idr(sawal_val),
        "dana_masuk": format_idr(dmasuk_val),
        "dana_keluar": format_idr(dkeluar_val),
        "saldo_akhir": format_idr(sakhir_val)
    }

    print(f"Header: {header}")
    print(f"Summary: {summary}")

    # Harvest 37 authentic descriptions, dates, and times from 2.pdf
    pdf_source = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\2.pdf"
    authentic_items = []
    with pdfplumber.open(pdf_source) as pdf:
        for p_idx, page in enumerate(pdf.pages):
            words = page.extract_words()
            min_top = 320 if p_idx == 0 else 200
            table_words = [w for w in words if min_top <= w["top"] <= 800]
            
            # find all 'WIB' occurrences
            wib_words = sorted([w for w in table_words if w['text'] == 'WIB'], key=lambda x: x['top'])
            for ww in wib_words:
                time_token = [w['text'] for w in table_words if abs(w['top'] - ww['top']) < 3 and w['x1'] <= ww['x0'] + 1]
                date_tokens = [w['text'] for w in table_words if 0 < (ww['top'] - w['top']) < 15 and 45 <= w['x0'] <= 90]
                
                # Extract multi-line description exactly as formatted in 2.pdf
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
                raw_d = " ".join(date_tokens).replace("Jan", "Aug").strip()
                d_str = re.sub(r'(\d+)\s*([A-Za-z]+)\s*(\d+)', r'\1 \2 \3', raw_d)

                authentic_items.append({
                    "date": d_str,
                    "time": t_str,
                    "desc": desc_text
                })

    print(f"Harvested {len(authentic_items)} authentic items (date, time, desc) from 2.pdf")
    assert len(authentic_items) == 37

    # Read 37 active transactions from Excel (including any custom Date / Time)
    excel_txs = []
    for r in range(6, ws2.max_row + 1):
        nom_cell = ws2.cell(r, 5).value
        sal_cell = ws2.cell(r, 7).value
        nom = parse_num(nom_cell)
        sal = parse_num(sal_cell)
        if abs(nom) > 0.001:
            date_cell = ws2.cell(r, 2).value
            time_cell = ws2.cell(r, 3).value
            
            # Format date if provided in Excel
            formatted_date_ex = None
            if date_cell:
                if isinstance(date_cell, datetime.datetime):
                    formatted_date_ex = date_cell.strftime("%d %b %Y")
                elif isinstance(date_cell, str):
                    formatted_date_ex = date_cell.strip()
                    
            # Format time if provided in Excel
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

    print(f"Harvested {len(excel_txs)} active transactions from Excel")
    assert len(excel_txs) == 37

    # Merge into 37 standardized transactions
    transactions = []
    for i in range(37):
        ex = excel_txs[i]
        auth = authentic_items[i]
        
        # Nominal & Tipe from Excel
        val = ex["nominal_num"]
        tipe = "CR" if val > 0 else "DB"
        formatted_nom = f"+{format_idr(val)}" if tipe == "CR" else f"-{format_idr(val)}"
        formatted_sal = format_idr(ex["saldo_num"])

        # Date & Time: prioritize Excel if specified, else authentic from 2.pdf
        date_val = ex["date_excel"] if ex["date_excel"] else auth["date"]
        time_val = ex["time_excel"] if ex["time_excel"] else auth["time"]

        # Description: 100% authentic, untouched from 2.pdf
        desc = auth["desc"]

        transactions.append({
            "no": i + 1,
            "tanggal": date_val,
            "jam": time_val,
            "uraian": desc,
            "nominal": formatted_nom,
            "tipe": tipe,
            "saldo": formatted_sal
        })

    # Assemble 4-page structure: Page 1 + Mid + Mid + Disclaimer Inline
    page_paths = [p1_template, p_mid_template, p_mid_template, p_disc_inline]
    temp_combined = os.path.join(os.path.dirname(output_pdf_path), "temp_galang_assembly.pdf")

    with PdfCraftClient() as client:
        client.call_tool("doc_combine", {
            "paths": page_paths,
            "out": temp_combined,
            "open": False
        })

        doc_id = client.doc_open(temp_combined)
        print(f"Editing assembled 4-page document (doc_id={doc_id})...")

        # 1. Apply Header across all 4 pages
        for p_num in range(1, 5):
            paras = client.get_paragraphs(doc_id, page=p_num)
            
            # Step A: Empty old Cabang paragraph to prevent collision
            p_cabang = [p for p in paras if ("Taman Aries" in p["text"] or "KCP" in p["text"] or "Ciceri" in p["text"]) and 115 <= p["rect"][1] <= 135 and p["rect"][0] < 200]
            if p_cabang:
                client.edit_text(doc_id, page=p_num, paragraph=p_cabang[0]["paragraph"], text="")

            # Step B: Apply 3-line composite block to Name paragraph
            # Line 1: GALANG PUTRA (at y0=99.92)
            # Line 2: KURNIAWAN (at y0=110.92)
            # Line 3: KCP Serang Ciceri (at y0=121.92)
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
                if ("01" in p["text"] and "Aug" in p["text"]) and 90 <= p["rect"][1] <= 115 and 330 <= p["rect"][0] <= 370:
                    client.edit_text(doc_id, page=p_num, paragraph=p["paragraph"], text=header["periode"])
                    break

            # Step D: Dicetak Pada
            paras = client.get_paragraphs(doc_id, page=p_num)
            for p in paras:
                if ("09" in p["text"] and "Sep" in p["text"]) and 115 <= p["rect"][1] <= 135 and 330 <= p["rect"][0] <= 370:
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
                    client.edit_text(doc_id, page=p_num, paragraph=p["paragraph"], text=f"{p_num} dari 4", width=50.0)
                elif "of" in p["text"] and 530 <= p["rect"][0] <= 570 and 105 <= p["rect"][1] <= 125:
                    client.edit_text(doc_id, page=p_num, paragraph=p["paragraph"], text=f"{p_num} of 4", width=50.0)

        # 2. Page 1 Account Number & Financial Summary
        paras = client.get_paragraphs(doc_id, page=1)
        for p in paras:
            if "1650003584860" in p["text"]:
                client.edit_text(doc_id, page=1, paragraph=p["paragraph"], text=f"{header['nomor_rekening']} ")
                break

        # Summary values
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

        # 3. Populate Transactions Page by Page
        page_capacities = [10, 12, 12, 3]
        tx_cursor = 0

        for p_idx, num_rows in enumerate(page_capacities):
            p_num = p_idx + 1
            base_y_start = 343.92 if p_num == 1 else 227.92
            max_template_rows = 10 if p_num == 1 else (12 if p_num in [2, 3] else 7)

            for r_i in range(num_rows):
                tx = transactions[tx_cursor]
                tx_cursor += 1
                row_y = base_y_start + r_i * 46.00

                # No (x0 ~ 20.00)
                paras = client.get_paragraphs(doc_id, page=p_num)
                p_no = [p for p in paras if abs(p["rect"][1] - row_y) < 15 and 15 <= p["rect"][0] <= 35 and p["text"].strip().isdigit()]
                if p_no:
                    client.edit_text(doc_id, page=p_num, paragraph=p_no[0]["paragraph"], text=str(tx["no"]))
                    up = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == p_no[0]["paragraph"]][0]
                    dx = COL_NO_X - up["rect"][0]
                    if abs(dx) > 0.05: client.edit_text(doc_id, page=p_num, paragraph=up["paragraph"], dx=dx)

                # Date: strictly targeted at y0 = row_y - 4.0 pt
                paras = client.get_paragraphs(doc_id, page=p_num)
                p_date = [p for p in paras if 45 <= p["rect"][0] <= 80 and abs(p["rect"][1] - (row_y - 4.0)) < 2.5]
                if p_date:
                    client.edit_text(doc_id, page=p_num, paragraph=p_date[0]["paragraph"], text=tx["tanggal"])
                    up = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == p_date[0]["paragraph"]][0]
                    dx = COL_DATE_TIME_X0 - up["rect"][0]
                    if abs(dx) > 0.05: client.edit_text(doc_id, page=p_num, paragraph=up["paragraph"], dx=dx)

                # Time: strictly targeted at y0 = row_y + 5.0 pt
                paras = client.get_paragraphs(doc_id, page=p_num)
                p_time = [p for p in paras if 45 <= p["rect"][0] <= 80 and abs(p["rect"][1] - (row_y + 5.0)) < 2.5]
                if p_time:
                    client.edit_text(doc_id, page=p_num, paragraph=p_time[0]["paragraph"], text=tx["jam"])
                    up = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == p_time[0]["paragraph"]][0]
                    dx = COL_DATE_TIME_X0 - up["rect"][0]
                    if abs(dx) > 0.05: client.edit_text(doc_id, page=p_num, paragraph=up["paragraph"], dx=dx)

                # Description: Vertical centering formula + 10 pt line spacing (exact Bank Mandiri layout)
                paras = client.get_paragraphs(doc_id, page=p_num)
                p_desc = [p for p in paras if abs(p["rect"][1] - row_y) < 20 and 120 <= p["rect"][0] <= 135]
                if p_desc:
                    num_lines = len(tx["uraian"].split("\n"))
                    target_y = row_y - (num_lines - 1) * 5.0
                    current_y = p_desc[0]["rect"][1]
                    dy = current_y - target_y
                    
                    client.call_tool("text_edit", {
                        "doc": doc_id,
                        "page": p_num,
                        "paragraph": p_desc[0]["paragraph"],
                        "text": tx["uraian"],
                        "dy": dy,
                        "line_spacing": 1.25,
                        "width": 230.0
                    })
                    up = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == p_desc[0]["paragraph"]][0]
                    dx = COL_DESC_X - up["rect"][0]
                    if abs(dx) > 0.05: client.edit_text(doc_id, page=p_num, paragraph=up["paragraph"], dx=dx)

                # Nominal (Right-aligned to 448.00 pt)
                paras = client.get_paragraphs(doc_id, page=p_num)
                p_nom = [p for p in paras if abs(p["rect"][1] - row_y) < 15 and 370 <= p["rect"][0] <= 450]
                if p_nom:
                    color = COLOR_CREDIT_GREEN if tx["tipe"] == "CR" else COLOR_DEBIT_BLACK
                    client.edit_text(doc_id, page=p_num, paragraph=p_nom[0]["paragraph"], text=tx["nominal"], color=color)
                    up = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == p_nom[0]["paragraph"]][0]
                    dx = COL_NOMINAL_RIGHT_X - up["rect"][2]
                    if abs(dx) > 0.01: client.edit_text(doc_id, page=p_num, paragraph=up["paragraph"], dx=dx)

                # Saldo (Right-aligned to 582.00 pt)
                paras = client.get_paragraphs(doc_id, page=p_num)
                p_sal = [p for p in paras if abs(p["rect"][1] - row_y) < 15 and 490 <= p["rect"][0] <= 585]
                if p_sal:
                    client.edit_text(doc_id, page=p_num, paragraph=p_sal[0]["paragraph"], text=tx["saldo"], color=COLOR_RUNNING_SALDO_BLUE)
                    up = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == p_sal[0]["paragraph"]][0]
                    dx = COL_SALDO_RIGHT_X - up["rect"][2]
                    if abs(dx) > 0.01: client.edit_text(doc_id, page=p_num, paragraph=up["paragraph"], dx=dx)

            # On Page 4: blank out unused rows 4 to 7
            if num_rows < max_template_rows:
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
    excel_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\Template_Mutasi_Aug.xlsx"
    out_pdf = r"output\REK_GALANG_AUG_2026_STANDARDIZED.pdf"
    build_galang_aug_statement(excel_path, out_pdf)
