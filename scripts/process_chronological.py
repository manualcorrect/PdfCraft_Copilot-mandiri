"""
Auto-Chronological Logic Implementation for Bank Mandiri Statements
Supports:
1. Detecting gaji or pivot date (e.g. 25th).
2. Auto-redistributing subsequent transactions chronologically between pivot date and month-end.
3. Preserving authentic timestamps from source PDF.
4. Writing back dates & times to Excel if desired.
5. Updating the PDF with 100% authentic untouched descriptions.
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

def process_statement_chronological(month_code: str, src_pdf_path: str, excel_path: str, out_pdf_path: str, sync_excel_path: str = None):
    print(f"\n{'='*20} PROCESSING {month_code} WITH AUTO-CHRONOLOGY {'='*20}")
    
    # 1. Read Excel Header & Financial Summary
    wb = openpyxl.load_workbook(excel_path, data_only=False)
    ws1 = wb["Header & Ringkasan"]
    ws2 = wb["Tabel_Mutasi"]

    cabang = str(ws1.cell(11, 2).value or "KCP Serang Ciceri").strip()
    periode = str(ws1.cell(12, 2).value or f"01 {month_code.capitalize()} 2026 - 30 {month_code.capitalize()} 2026").strip()
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

    # 2. Extract authentic dates, times, and paragraphs from source PDF
    pdf_tx_meta = []
    total_pages = 0
    with pdfplumber.open(src_pdf_path) as pdf:
        total_pages = len(pdf.pages)
        for p_idx, page in enumerate(pdf.pages):
            words = page.extract_words()
            min_top = 320 if p_idx == 0 else 200
            table_words = [w for w in words if min_top <= w["top"] <= 800]
            wibs = sorted([w for w in table_words if w["text"] == "WIB"], key=lambda x: x["top"])
            for w in wibs:
                time_w = [x["text"] for x in table_words if abs(x["top"] - w["top"]) < 3 and x["x1"] <= w["x0"] + 1]
                t_str = f"{time_w[-1]} WIB" if time_w else "12:00:00 WIB"
                
                date_w = [x["text"] for x in table_words if 0 < (w["top"] - x["top"]) < 15 and 45 <= x["x0"] <= 95]
                raw_d = " ".join(date_w).strip()
                # Extract day number
                m = re.search(r'^(\d+)', raw_d)
                day_num = int(m.group(1)) if m else 1
                
                pdf_tx_meta.append({
                    "page": p_idx + 1,
                    "top": w["top"],
                    "orig_day": day_num,
                    "orig_date_str": raw_d,
                    "orig_time_str": t_str
                })

    print(f"Read {len(pdf_tx_meta)} physical transactions from {src_pdf_path}")

    # 3. Read Excel transactions
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
        
        d_val = None
        if date_cell:
            if isinstance(date_cell, datetime.datetime):
                d_val = date_cell.strftime("%d %b %Y")
            else:
                d_val = str(date_cell).strip()
                
        t_val = None
        if time_cell:
            t_str = str(time_cell).strip()
            if "WIB" not in t_str: t_str = f"{t_str} WIB"
            t_val = t_str

        excel_txs.append({
            "excel_row": r,
            "nom": nom,
            "sal": sal,
            "date_in": d_val,
            "time_in": t_val
        })

    assert len(excel_txs) == len(pdf_tx_meta), f"Excel tx count ({len(excel_txs)}) != PDF count ({len(pdf_tx_meta)})"

    # 4. Unified Chronological Continuation Engine
    last_day_of_month = 30 if month_code.upper() in ["SEP", "APR", "JUN", "NOV"] else 31

    def get_month_abbr(code):
        c = code.upper()
        if c in ["OCT", "OKT"]: return "Oct"
        if c in ["AUG", "AGU"]: return "Aug"
        return c.capitalize()

    month_abbr = get_month_abbr(month_code)
    periode = periode.replace("Okt", "Oct").replace("OKT", "Oct")

    def parse_day(val):
        if isinstance(val, (datetime.date, datetime.datetime)):
            return val.day
        s = str(val).strip()
        m_iso = re.search(r'^\d{4}-\d{2}-(\d{2})', s)
        if m_iso: return int(m_iso.group(1))
        m_std = re.search(r'^(\d{1,2})\s+[A-Za-z]+', s)
        if m_std: return int(m_std.group(1))
        m_any = re.search(r'(\d{1,2})', s)
        return int(m_any.group(1)) if m_any else 25

    def format_date_str(val, fallback_day):
        if isinstance(val, (datetime.date, datetime.datetime)):
            return val.strftime(f"%d {month_abbr} %Y")
        if val:
            s = str(val).strip()
            m_iso = re.search(r'^(\d{4})-(\d{2})-(\d{2})', s)
            if m_iso:
                return f"{int(m_iso.group(3)):02d} {month_abbr} {m_iso.group(1)}"
            s = s.replace("Okt", "Oct").replace("OKT", "Oct")
            return s
        return f"{fallback_day:02d} {month_abbr} 2026"

    # Find pivot date (e.g. Gaji entered as 25 Sep)
    pivot_idx = None
    pivot_day = 25
    for i, ex in enumerate(excel_txs):
        if ex["date_in"] and ("25" in str(ex["date_in"]) or ex["nom"] > 5000000):
            pivot_idx = i
            pivot_day = parse_day(ex["date_in"])
            break

    if pivot_idx is None:
        pivot_idx = max(range(len(excel_txs)), key=lambda i: excel_txs[i]["nom"])
        pivot_day = 25

    print(f"Pivot transaction detected at Tx {pivot_idx + 1 if pivot_idx is not None else 'None'} (Day: {pivot_day})")

    # Schedule array
    schedule = [None] * len(excel_txs)

    # Fill pre-pivot and explicit entries
    for i in range(len(excel_txs)):
        if i <= pivot_idx:
            d_str = format_date_str(excel_txs[i]["date_in"], pdf_tx_meta[i]["orig_day"])
            t_str = excel_txs[i]["time_in"] or pdf_tx_meta[i]["orig_time_str"]
            schedule[i] = {"date": d_str, "time": t_str}
        else:
            if excel_txs[i]["date_in"]:
                d_str = format_date_str(excel_txs[i]["date_in"], pdf_tx_meta[i]["orig_day"])
                t_str = excel_txs[i]["time_in"] or pdf_tx_meta[i]["orig_time_str"]
                schedule[i] = {"date": d_str, "time": t_str}

    # Auto-chronology for remaining post-pivot entries
    post_indices = [i for i in range(pivot_idx + 1, len(excel_txs)) if schedule[i] is None]
    if post_indices:
        last_idx = post_indices[-1]
        is_closing_fee = (last_idx == len(excel_txs) - 1)
        intermediate_indices = post_indices[:-1] if is_closing_fee else post_indices

        groups = []
        curr_group = []
        for idx in intermediate_indices:
            t_str = pdf_tx_meta[idx]["orig_time_str"]
            d_orig = pdf_tx_meta[idx]["orig_day"]
            if not curr_group:
                curr_group.append(idx)
            else:
                prev_idx = curr_group[-1]
                prev_t = pdf_tx_meta[prev_idx]["orig_time_str"]
                prev_d = pdf_tx_meta[prev_idx]["orig_day"]
                if t_str == prev_t or (d_orig == prev_d and abs(excel_txs[idx]["nom"]) in [1000, 2500, 1500, 3500]):
                    curr_group.append(idx)
                elif d_orig == prev_d and len(curr_group) < 3 and month_code.upper() == "SEP":
                    curr_group.append(idx)
                else:
                    groups.append(curr_group)
                    curr_group = [idx]
        if curr_group:
            groups.append(curr_group)

        num_groups = len(groups)
        avail_days = (last_day_of_month - 1) - pivot_day
        for g_i, grp in enumerate(groups):
            assigned_day = pivot_day + int(g_i * (avail_days / max(1, num_groups - 1))) if num_groups > 1 else pivot_day
            assigned_day = min(assigned_day, last_day_of_month - 1)
            for idx in grp:
                d_str = f"{assigned_day:02d} {month_abbr} 2026"
                t_str = excel_txs[idx]["time_in"] or pdf_tx_meta[idx]["orig_time_str"]
                schedule[idx] = {"date": d_str, "time": t_str}

        if is_closing_fee:
            schedule[last_idx] = {
                "date": f"{last_day_of_month:02d} {month_abbr} 2026",
                "time": excel_txs[last_idx]["time_in"] or "23:59:00 WIB"
            }

    final_txs = []
    for i in range(len(excel_txs)):
        ex = excel_txs[i]
        final_txs.append({
            "no": i + 1,
            "excel_row": ex["excel_row"],
            "date": schedule[i]["date"],
            "time": schedule[i]["time"],
            "nom": ex["nom"],
            "sal": ex["sal"],
            "is_credit": ex["nom"] > 0
        })

    print("Sample chronological progression:")
    for t in final_txs[max(0, (pivot_idx or 20) - 2) : min(len(final_txs), (pivot_idx or 20) + 7)]:
        print(f"  Tx {t['no']:2d}: {t['date']} {t['time']} | Nom: {t['nom']:>12,.2f} | Saldo: {t['sal']:>12,.2f}")

    # 5. Sync back to Excel if requested
    if sync_excel_path:
        print(f"Syncing chronological dates & times to Excel: {sync_excel_path}...")
        sync_wb = openpyxl.load_workbook(sync_excel_path)
        sync_ws2 = sync_wb["Tabel_Mutasi"]
        for t in final_txs:
            row_idx = t["excel_row"]
            sync_ws2.cell(row_idx, 1).value = t["no"]
            sync_ws2.cell(row_idx, 2).value = t["date"]
            sync_ws2.cell(row_idx, 3).value = t["time"]
        sync_wb.save(sync_excel_path)
        print("Excel synchronized successfully!")

    # 6. Apply direct edits to PDF
    shutil.copyfile(src_pdf_path, out_pdf_path)

    with PdfCraftClient() as client:
        doc_id = client.doc_open(out_pdf_path)
        print(f"Applying direct updates to {out_pdf_path}...")

        # Edit Headers across all pages
        for p_num in range(1, total_pages + 1):
            paras = client.get_paragraphs(doc_id, page=p_num)
            
            # Step A: Empty old Cabang paragraph to avoid collision
            p_cabang = [p for p in paras if ("Taman Aries" in p["text"] or "KCP" in p["text"] or "Ciceri" in p["text"]) and 115 <= p["rect"][1] <= 135 and p["rect"][0] < 200]
            if p_cabang:
                client.edit_text(doc_id, page=p_num, paragraph=p_cabang[0]["paragraph"], text="")

            # Step B: 3-line composite block: GALANG PUTRA / KURNIAWAN / KCP Serang Ciceri
            paras = client.get_paragraphs(doc_id, page=p_num)
            p_name = [p for p in paras if ("ROY DARWIN" in p["text"] or "GALANG" in p["text"]) and 90 <= p["rect"][1] <= 115 and p["rect"][0] < 200]
            if p_name:
                composite_text = f"GALANG PUTRA\nKURNIAWAN\n{cabang}"
                kwargs_name = {"line_spacing": 1.375}
                if month_code.upper() in ["OCT", "OKT"]:
                    kwargs_name["font"] = "helvetica"
                client.call_tool("text_edit", {
                    "doc": doc_id, "page": p_num, "paragraph": p_name[0]["paragraph"],
                    "text": composite_text, **kwargs_name
                })
                up_p = [x for x in client.get_paragraphs(doc_id, page=p_num) if x["paragraph"] == p_name[0]["paragraph"]][0]
                dx = VALUE_COL1_X0 - up_p["rect"][0]
                if abs(dx) > 0.05:
                    client.edit_text(doc_id, page=p_num, paragraph=p_name[0]["paragraph"], dx=dx)

            # Step C: Periode
            paras = client.get_paragraphs(doc_id, page=p_num)
            for p in paras:
                if ("01" in p["text"] and any(m in p["text"] for m in ["Jan", "Feb", "Aug", "Sep", "Oct", "Okt"])) and 90 <= p["rect"][1] <= 115 and 330 <= p["rect"][0] <= 370:
                    kwargs_per = {}
                    if month_code.upper() in ["OCT", "OKT"]:
                        kwargs_per["font"] = "helvetica"
                    client.call_tool("text_edit", {
                        "doc": doc_id, "page": p_num, "paragraph": p["paragraph"],
                        "text": periode, **kwargs_per
                    })
                    break

            # Step D: Dicetak Pada
            paras = client.get_paragraphs(doc_id, page=p_num)
            for p in paras:
                if any(m in p["text"] for m in ["Sep", "Nov"]) and 115 <= p["rect"][1] <= 135 and 330 <= p["rect"][0] <= 370:
                    client.edit_text(doc_id, page=p_num, paragraph=p["paragraph"], text=dicetak_pada)
                    break

            # Step E: Page Numbers: empty standalone '8' or '7', change 'X dari 8' -> 'X dari 4', 'X of 8' -> 'X of 4'
            paras = client.get_paragraphs(doc_id, page=p_num)
            for p in paras:
                if p["text"].strip().isdigit() and 545 <= p["rect"][0] <= 575 and 90 <= p["rect"][1] <= 110:
                    client.edit_text(doc_id, page=p_num, paragraph=p["paragraph"], text="")

            paras = client.get_paragraphs(doc_id, page=p_num)
            for p in paras:
                if "dari" in p["text"] and 520 <= p["rect"][0] <= 570 and 90 <= p["rect"][1] <= 115:
                    client.edit_text(doc_id, page=p_num, paragraph=p["paragraph"], text=f"{p_num} dari {total_pages}", width=50.0)
                elif "of" in p["text"] and 530 <= p["rect"][0] <= 570 and 105 <= p["rect"][1] <= 125:
                    kwargs_of = {"width": 50.0}
                    if month_code.upper() in ["OCT", "OKT"]:
                        kwargs_of["font"] = "helvetica"
                        kwargs_of["italic"] = True
                    client.call_tool("text_edit", {
                        "doc": doc_id, "page": p_num, "paragraph": p["paragraph"],
                        "text": f"{p_num} of {total_pages}", **kwargs_of
                    })

        # Page 1 Account Number & Summary
        paras = client.get_paragraphs(doc_id, page=1)
        for p in paras:
            if "1650003584860" in p["text"] or "1660003584860" in p["text"] or "1630016287487" in p["text"]:
                client.edit_text(doc_id, page=1, paragraph=p["paragraph"], text=nomor_rekening)
                up_acc = [x for x in client.get_paragraphs(doc_id, page=1) if x["paragraph"] == p["paragraph"]][0]
                dx = 160.00 - up_acc["rect"][0]
                if abs(dx) > 0.05:
                    client.edit_text(doc_id, page=1, paragraph=p["paragraph"], dx=dx)
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

        # Process Transactions dynamically per page
        page_capacities = [sum(1 for m in pdf_tx_meta if m["page"] == p) for p in range(1, total_pages + 1)]
        tx_cursor = 0

        for p_idx, num_rows in enumerate(page_capacities):
            p_num = p_idx + 1
            if num_rows == 0:
                continue

            base_y_start = 343.92 if p_num == 1 else 227.92

            for r_i in range(num_rows):
                tx = final_txs[tx_cursor]
                tx_cursor += 1
                row_y = base_y_start + r_i * 46.00

                nom_str = ("+" if tx["is_credit"] else "-") + format_idr(tx["nom"])
                sal_str = format_idr(tx["sal"])

                # A. Update Date
                paras = client.get_paragraphs(doc_id, page=p_num)
                p_dates = [p for p in paras if 45 <= p["rect"][0] <= 85 and abs(p["rect"][1] - (row_y - 4.0)) < 10.0 and "WIB" not in p["text"]]
                if p_dates:
                    kwargs_date = {}
                    if month_code.upper() in ["OCT", "OKT"]:
                        kwargs_date["font"] = "helvetica"
                    client.call_tool("text_edit", {
                        "doc": doc_id, "page": p_num, "paragraph": p_dates[0]["paragraph"],
                        "text": tx["date"], **kwargs_date
                    })

                # B. Update Time
                paras = client.get_paragraphs(doc_id, page=p_num)
                p_times = [p for p in paras if 45 <= p["rect"][0] <= 85 and abs(p["rect"][1] - (row_y + 5.0)) < 10.0 and "WIB" in p["text"]]
                if p_times:
                    client.edit_text(doc_id, page=p_num, paragraph=p_times[0]["paragraph"], text=tx["time"])

                # C. Update Nominal
                paras = client.get_paragraphs(doc_id, page=p_num)
                p_noms = [p for p in paras if abs(p["rect"][1] - row_y) < 15 and 370 <= p["rect"][0] <= 450]
                if p_noms:
                    col = COLOR_CREDIT_GREEN if tx["is_credit"] else COLOR_DEBIT_BLACK
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

                # E. If original text had '83 Biaya saldo minimum' on closing tx (in 3.pdf), update to current row count
                if tx["no"] == len(final_txs) and p_num == total_pages:
                    paras = client.get_paragraphs(doc_id, page=p_num)
                    p_83 = [p for p in paras if p["text"].strip().startswith("83") and "saldo minimum" in p["text"]]
                    if p_83:
                        client.edit_text(doc_id, page=p_num, paragraph=p_83[0]["paragraph"], text=f"{tx['no']} Biaya saldo minimum")

                # Keterangan is 100% untouched!

        client.doc_save(doc_id, path=out_pdf_path, full=True)
        client.doc_close(doc_id)
        print(f"\n[DONE] Successfully generated statement: {out_pdf_path}")

if __name__ == "__main__":
    target = sys.argv[1].upper() if len(sys.argv) > 1 else "ALL"
    
    if target in ["SEP", "ALL"]:
        sep_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\3.pdf"
        sep_excel = r"output\Template_Mutasi_SEP_Reconciled.xlsx"
        sep_out = "output/REK_GALANG_SEP_2026_CHRONOLOGICAL.pdf"
        process_statement_chronological("SEP", sep_pdf, sep_excel, sep_out, sync_excel_path=sep_excel)

    if target in ["OCT", "ALL"]:
        oct_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\1.pdf"
        oct_excel = r"output\Template_Mutasi_OCT_Reconciled.xlsx"
        oct_out = "output/REK_GALANG_OCT_2026_CHRONOLOGICAL.pdf"
        process_statement_chronological("OCT", oct_pdf, oct_excel, oct_out, sync_excel_path=oct_excel)
