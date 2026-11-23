import re
import datetime
import openpyxl
import pdfplumber

def test_month(month_code, pdf_path, excel_path):
    print(f"\n{'='*25} TESTING {month_code} {'='*25}")
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    ws2 = wb["Tabel_Mutasi"]
    
    excel_txs = []
    for r in range(6, ws2.max_row + 1):
        nom_cell = ws2.cell(r, 5).value
        if nom_cell is None or str(nom_cell).strip() == '':
            continue
        nom = float(str(nom_cell).replace("Rp", "").replace(".", "").replace(",", ".").strip())
        d_val = ws2.cell(r, 2).value
        t_val = ws2.cell(r, 3).value
        excel_txs.append({
            "row": r,
            "nom": nom,
            "date_in": str(d_val).strip() if d_val else None,
            "time_in": str(t_val).strip() if t_val else None
        })
        
    pdf_tx_meta = []
    with pdfplumber.open(pdf_path) as pdf:
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
                m = re.search(r'^(\d+)', raw_d)
                day_num = int(m.group(1)) if m else 1
                pdf_tx_meta.append({
                    "page": p_idx + 1,
                    "orig_day": day_num,
                    "orig_time_str": t_str
                })

    last_day_of_month = 30 if month_code.upper() in ["SEP", "APR", "JUN", "NOV"] else 31
    
    def parse_day(val):
        if isinstance(val, (datetime.date, datetime.datetime)):
            return val.day
        s = str(val).strip()
        # ISO format: YYYY-MM-DD
        m_iso = re.search(r'^\d{4}-\d{2}-(\d{2})', s)
        if m_iso: return int(m_iso.group(1))
        # Standard: DD Mon YYYY
        m_std = re.search(r'^(\d{1,2})\s+[A-Za-z]+', s)
        if m_std: return int(m_std.group(1))
        # Fallback
        m_any = re.search(r'(\d{1,2})', s)
        return int(m_any.group(1)) if m_any else 25

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

    schedule = [None] * len(excel_txs)
    
    for i in range(len(excel_txs)):
        if i <= pivot_idx:
            if excel_txs[i]["date_in"]:
                d_str = excel_txs[i]["date_in"]
            else:
                d_num = pdf_tx_meta[i]["orig_day"]
                d_str = f"{d_num:02d} {month_code.capitalize()} 2026"
            t_str = excel_txs[i]["time_in"] or pdf_tx_meta[i]["orig_time_str"]
            schedule[i] = {"date": d_str, "time": t_str}
        else:
            if excel_txs[i]["date_in"]:
                schedule[i] = {"date": excel_txs[i]["date_in"], "time": excel_txs[i]["time_in"] or pdf_tx_meta[i]["orig_time_str"]}

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
            
        print("Groups generated:", groups)
            
        num_groups = len(groups)
        avail_days = (last_day_of_month - 1) - pivot_day
        for g_i, grp in enumerate(groups):
            assigned_day = pivot_day + int(g_i * (avail_days / max(1, num_groups - 1))) if num_groups > 1 else pivot_day
            assigned_day = min(assigned_day, last_day_of_month - 1)
            for idx in grp:
                d_str = f"{assigned_day:02d} {month_code.capitalize()} 2026"
                t_str = excel_txs[idx]["time_in"] or pdf_tx_meta[idx]["orig_time_str"]
                schedule[idx] = {"date": d_str, "time": t_str}
                
        if is_closing_fee:
            schedule[last_idx] = {
                "date": f"{last_day_of_month:02d} {month_code.capitalize()} 2026",
                "time": excel_txs[last_idx]["time_in"] or "23:59:00 WIB"
            }

    print(f"Total transactions: {len(schedule)} | Pivot at Tx {pivot_idx + 1}")
    for i in range(max(0, pivot_idx - 1), len(schedule)):
        print(f"  Tx {i+1:2d}: {schedule[i]['date']} {schedule[i]['time']} | Nom: {excel_txs[i]['nom']:>12,.2f}")

test_month("SEP", r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\3.pdf", r"output\Template_Mutasi_SEP_Reconciled.xlsx")
test_month("OCT", r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\1.pdf", r"output\Template_Mutasi_OCT_Reconciled.xlsx")
