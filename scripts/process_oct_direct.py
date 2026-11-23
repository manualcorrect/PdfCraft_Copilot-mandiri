"""
Process October Statement Directly from 1.pdf
Maintains 100% authentic, untouched descriptions from 1.pdf.
Zero text collisions, zero distortion.
"""

import os
import sys
import shutil
import re
import datetime
import openpyxl
import pdfplumber

sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient
from bank_mandiri_spec import (
    COL_NOMINAL_RIGHT_X,
    COL_SALDO_RIGHT_X,
    SUMMARY_RIGHT_X,
    COL_NO_X,
    COL_DATE_TIME_X0,
    VALUE_COL1_X0,
    COLOR_CREDIT_GREEN,
    COLOR_RUNNING_SALDO_BLUE,
    COLOR_DEBIT_BLACK,
    COLOR_SALDO_AWAL_GRAY
)

def format_idr(num):
    return f"{abs(num):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def parse_num(val):
    if val is None: return 0.0
    if isinstance(val, (int, float)): return float(val)
    s = str(val).replace("Rp", "").replace(" ", "").replace(".", "").replace(",", ".").strip()
    try: return float(s)
    except: return 0.0

src_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\1.pdf"
excel_path = r"output\Template_Mutasi_OCT_Reconciled.xlsx"
out_pdf = "output/REK_GALANG_OCT_2026_DIRECT.pdf"

print("="*20, "PROCESSING OCT DIRECTLY FROM 1.PDF", "="*20)

wb = openpyxl.load_workbook(excel_path, data_only=True)
ws1 = wb["Header & Ringkasan"]
ws2 = wb["Tabel_Mutasi"]

cabang = str(ws1.cell(11, 2).value or "KCP Serang Ciceri").strip()
periode = str(ws1.cell(12, 2).value or "01 Oct 2026 - 31 Oct 2026").strip()
dicetak_cell = ws1.cell(13, 2).value
if isinstance(dicetak_cell, datetime.datetime):
    dicetak_pada = dicetak_cell.strftime("%d %b %Y")
else:
    dicetak_pada = str(dicetak_cell or "05 Nov 2026").strip()
nomor_rekening = str(ws1.cell(14, 2).value or "1630016287487").strip()

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

print("Summary:", summary)

# Read 34 active transactions
excel_txs = []
for r in range(6, ws2.max_row + 1):
    nom_cell = ws2.cell(r, 5).value
    sal_cell = ws2.cell(r, 7).value
    if nom_cell is None or str(nom_cell).strip() == '':
        continue
    nom = parse_num(nom_cell)
    sal = parse_num(sal_cell)
    
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
        "row": r,
        "nom": nom,
        "sal": sal,
        "date_ex": formatted_date_ex,
        "time_ex": formatted_time_ex
    })

print(f"Loaded {len(excel_txs)} transactions from Excel OCT")
assert len(excel_txs) == 34, f"Expected 34 txs, got {len(excel_txs)}"

shutil.copyfile(src_pdf, out_pdf)

with PdfCraftClient() as client:
    doc_id = client.doc_open(out_pdf)
    print(f"Editing {out_pdf} directly...")
    
    # Headers across pages 1, 2, 3 (Page 4 is standalone disclaimer without header)
    for p_num in range(1, 4):
        paras = client.get_paragraphs(doc_id, page=p_num)
        
        p_cabang = [p for p in paras if ("Taman Aries" in p["text"] or "KCP" in p["text"] or "Ciceri" in p["text"]) and 115 <= p["rect"][1] <= 135 and p["rect"][0] < 200]
        if p_cabang:
            client.edit_text(doc_id, page=p_num, paragraph=p_cabang[0]["paragraph"], text="")

        paras = client.get_paragraphs(doc_id, page=p_num)
        p_name = [p for p in paras if ("ROY DARWIN" in p["text"] or "GALANG" in p["text"]) and 90 <= p["rect"][1] <= 115 and p["rect"][0] < 200]
        if p_name:
            composite_text = f"GALANG PUTRA\nKURNIAWAN\n{cabang}"
            client.edit_text(doc_id, page=p_num, paragraph=p_name[0]["paragraph"], text=composite_text, line_spacing=1.375)
            up_p = [x for x in client.get_paragraphs(doc_id, page=p_num) if x["paragraph"] == p_name[0]["paragraph"]][0]
            dx = VALUE_COL1_X0 - up_p["rect"][0]
            if abs(dx) > 0.05:
                client.edit_text(doc_id, page=p_num, paragraph=p_name[0]["paragraph"], dx=dx)

        paras = client.get_paragraphs(doc_id, page=p_num)
        for p in paras:
            if ("01" in p["text"] and any(m in p["text"] for m in ["Jan", "Feb", "Aug", "Sep", "Oct"])) and 90 <= p["rect"][1] <= 115 and 330 <= p["rect"][0] <= 370:
                client.edit_text(doc_id, page=p_num, paragraph=p["paragraph"], text=periode)
                break

        paras = client.get_paragraphs(doc_id, page=p_num)
        for p in paras:
            if any(m in p["text"] for m in ["Sep", "Nov"]) and 115 <= p["rect"][1] <= 135 and 330 <= p["rect"][0] <= 370:
                client.edit_text(doc_id, page=p_num, paragraph=p["paragraph"], text=dicetak_pada)
                break

        # Page numbering: e.g. "1 dari 4", "1 of 4"
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

    # Page 1 Account Number & Summary
    paras = client.get_paragraphs(doc_id, page=1)
    for p in paras:
        if "1650003584860" in p["text"] or "1660003584860" in p["text"]:
            client.edit_text(doc_id, page=1, paragraph=p["paragraph"], text=f"{nomor_rekening} ")
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

    # Process 34 Transactions (Page 1: 10, Page 2: 12, Page 3: 12)
    page_capacities = [10, 12, 12]
    tx_cursor = 0

    for p_idx, num_rows in enumerate(page_capacities):
        p_num = p_idx + 1
        base_y_start = 343.92 if p_num == 1 else 227.92

        for r_i in range(num_rows):
            tx = excel_txs[tx_cursor]
            tx_cursor += 1
            row_y = base_y_start + r_i * 46.00

            is_credit = tx["nom"] > 0
            nom_str = ("+" if is_credit else "-") + format_idr(tx["nom"])
            sal_str = format_idr(tx["sal"])

            # A. Update Date: replace Jan with Oct, or use custom date from Excel
            paras = client.get_paragraphs(doc_id, page=p_num)
            p_dates = [p for p in paras if 45 <= p["rect"][0] <= 85 and abs(p["rect"][1] - (row_y - 4.0)) < 10.0 and "WIB" not in p["text"]]
            if p_dates:
                cur_date = p_dates[0]["text"].replace("Jan", "Oct").strip()
                new_date = tx["date_ex"] if tx["date_ex"] else cur_date
                client.edit_text(doc_id, page=p_num, paragraph=p_dates[0]["paragraph"], text=new_date)

            # B. Update Time: if Excel has custom time (e.g. Gaji 04:00:00 WIB)
            if tx["time_ex"]:
                paras = client.get_paragraphs(doc_id, page=p_num)
                p_times = [p for p in paras if 45 <= p["rect"][0] <= 85 and abs(p["rect"][1] - (row_y + 5.0)) < 10.0 and "WIB" in p["text"]]
                if p_times:
                    client.edit_text(doc_id, page=p_num, paragraph=p_times[0]["paragraph"], text=tx["time_ex"])

            # C. Update Nominal
            paras = client.get_paragraphs(doc_id, page=p_num)
            p_noms = [p for p in paras if abs(p["rect"][1] - row_y) < 15 and 370 <= p["rect"][0] <= 450]
            if p_noms:
                col = COLOR_CREDIT_GREEN if is_credit else COLOR_DEBIT_BLACK
                client.edit_text(doc_id, page=p_num, paragraph=p_noms[0]["paragraph"], text=nom_str, color=col)
                up = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == p_noms[0]["paragraph"]][0]
                dx = COL_NOMINAL_RIGHT_X - up["rect"][2]
                if abs(dx) > 0.01: client.edit_text(doc_id, page=p_num, paragraph=up["paragraph"], dx=dx)

            # D. Update Saldo
            paras = client.get_paragraphs(doc_id, page=p_num)
            p_sals = [p for p in paras if abs(p["rect"][1] - row_y) < 15 and 490 <= p["rect"][0] <= 585]
            if p_sals:
                client.edit_text(doc_id, page=p_num, paragraph=p_sals[0]["paragraph"], text=sal_str, color=COLOR_RUNNING_SALDO_BLUE)
                up = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == p_sals[0]["paragraph"]][0]
                dx = COL_SALDO_RIGHT_X - up["rect"][2]
                if abs(dx) > 0.01: client.edit_text(doc_id, page=p_num, paragraph=up["paragraph"], dx=dx)

            # NOTICE: KETERANGAN IS 100% UNTOUCHED!

    client.doc_save(doc_id, path=out_pdf, full=True)
    client.doc_close(doc_id)
    print(f"\n[DONE] Successfully generated perfect OCT statement: {out_pdf}")

if __name__ == "__main__":
    pass
