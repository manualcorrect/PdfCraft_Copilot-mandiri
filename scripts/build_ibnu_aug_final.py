"""
Master Production Builder for Bank Mandiri e-Statement:
Client: IBNU AGUN
Period: August 2026 (01 Aug 2026 - 31 Aug 2026)
Source Directory: D:\\X_Files\\rekening\\PT BENDI NASHA NIAGA INDUSTRI\\Ibnu Agun\\Folder Baru\\aug

Produces:
1. Template_Mutasi_AUG_OUTPUT_1.xlsx
2. REK_IBNU_AUG_OUTPUT_1.pdf
"""

import os
import sys
import shutil
import re
import zlib
import datetime
import openpyxl
import pdfplumber
from PIL import Image

sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient
from bank_mandiri_spec import (
    COL_NOMINAL_RIGHT_X,
    COL_SALDO_RIGHT_X,
    SUMMARY_RIGHT_X,
    COL_DATE_TIME_X0,
    VALUE_COL1_X0,
    VALUE_COL2_X0,
    VALUE_ACC_X0,
    COLOR_CREDIT_GREEN,
    COLOR_RUNNING_SALDO_BLUE,
    COLOR_DEBIT_BLACK,
    COLOR_SALDO_AWAL_GRAY
)

BASE_DIR = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug"
EXCEL_IN = os.path.join(BASE_DIR, "Template_Mutasi_AUG.xlsx")
PDF_IN = os.path.join(BASE_DIR, "0.pdf")

WORKSPACE_OUT = r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output"
os.makedirs(WORKSPACE_OUT, exist_ok=True)
EXCEL_OUT = os.path.join(WORKSPACE_OUT, "Template_Mutasi_AUG_OUTPUT_1.xlsx")
PDF_OUT = os.path.join(WORKSPACE_OUT, "REK_IBNU_AUG_OUTPUT_1.pdf")

def format_idr(num: float) -> str:
    return f"{abs(num):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def to_hex(text: str) -> str:
    return ''.join(f'{ord(c):04X}' for c in text)

def to_utf16_be(text: str) -> bytes:
    res = bytearray()
    for ch in text:
        val = ord(ch)
        res.append((val >> 8) & 0xFF)
        res.append(val & 0xFF)
    return bytes(res)

def run():
    print("=================================================================")
    print("BUILDING IBNU AGUN - AUGUST 2026 (FINAL PERFECT)")
    print("=================================================================")

    # -----------------------------------------------------------------
    # STEP 1: EXTRACT TIMESTAMPS & GENERATE SYNCHRONIZED SCHEDULE
    # -----------------------------------------------------------------
    print("\n--- STEP 1: EXTRACTING TIMESTAMPS & SYNCHRONIZING SCHEDULE ---")
    pdf_tx_meta = []
    with pdfplumber.open(PDF_IN) as pdf:
        for p_idx, page in enumerate(pdf.pages):
            words = page.extract_words()
            min_top = 310 if p_idx == 0 else 180
            table_words = [w for w in words if min_top <= w['top'] <= 780]
            wibs = sorted([w for w in table_words if w['text'] == 'WIB'], key=lambda x: x['top'])
            for w in wibs:
                t_candidates = [x for x in table_words if abs(x['top'] - w['top']) < 3 and x['x1'] <= w['x0'] + 1]
                time_str = f"{t_candidates[-1]['text']} WIB" if t_candidates else '12:00:00 WIB'
                d_candidates = [x for x in table_words if 0 < (w['top'] - x['top']) < 15 and 45 <= x['x0'] <= 95]
                d_candidates.sort(key=lambda x: x['x0'])
                d_str = " ".join([x['text'] for x in d_candidates])
                m = re.search(r'^(\d+)', d_str)
                day_num = int(m.group(1)) if m else 1
                pdf_tx_meta.append({
                    'orig_day': day_num,
                    'orig_time': time_str,
                    'orig_date': d_str
                })

    assert len(pdf_tx_meta) == 75, f"Expected 75 tx in 0.pdf, found {len(pdf_tx_meta)}"
    print(f"Extracted {len(pdf_tx_meta)} transaction metadata entries from 0.pdf.")

    sal_idx = 59  # Tx 60 in 1-based indexing (Salary Row 67 in Excel)
    schedule = [None] * 75

    # Pre-salary groups (Tx 1..59)
    pre_groups = []
    seen = {}
    for i in range(sal_idx):
        key = (pdf_tx_meta[i]['orig_day'], pdf_tx_meta[i]['orig_time'])
        if key not in seen:
            seen[key] = len(pre_groups)
            pre_groups.append({
                'key': key,
                'indices': [i],
                'day': pdf_tx_meta[i]['orig_day'],
                'time': pdf_tx_meta[i]['orig_time']
            })
        else:
            pre_groups[seen[key]]['indices'].append(i)

    print(f"Identified {len(pre_groups)} pre-salary synchronized groups.")
    start_pre = datetime.datetime(2026, 8, 1, 8, 45, 0)
    end_pre = datetime.datetime(2026, 8, 24, 18, 15, 0)
    pre_span = (end_pre - start_pre).total_seconds()
    step_pre = pre_span / max(1, len(pre_groups))

    prev_dt = start_pre
    for g_idx, g in enumerate(pre_groups):
        cur_dt = start_pre + datetime.timedelta(seconds=g_idx * step_pre + ((g_idx * 137) % 720))
        if cur_dt.hour < 8:
            cur_dt = cur_dt.replace(hour=8, minute=20 + (g_idx * 3 % 35))
        elif cur_dt.hour >= 23:
            cur_dt = cur_dt.replace(hour=21, minute=15 + (g_idx * 5 % 30))
        if cur_dt <= prev_dt:
            cur_dt = prev_dt + datetime.timedelta(minutes=2, seconds=30)
        prev_dt = cur_dt

        d_str = f"{cur_dt.day:02d} Aug 2026"
        t_str = f"{cur_dt.strftime('%H:%M:%S')} WIB"
        for idx in g['indices']:
            schedule[idx] = {'date': d_str, 'time': t_str, 'dt': cur_dt}

    # Salary Tx 60
    schedule[sal_idx] = {
        'date': '25 Aug 2026',
        'time': '04:00:00 WIB',
        'dt': datetime.datetime(2026, 8, 25, 4, 0, 0)
    }

    # Closing Fee Tx 75
    schedule[74] = {
        'date': '31 Aug 2026',
        'time': '23:59:00 WIB',
        'dt': datetime.datetime(2026, 8, 31, 23, 59, 0)
    }

    # Post-salary intermediate groups (Tx 61..74)
    post_groups = []
    p_seen = {}
    for i in range(sal_idx + 1, 74):
        key = (pdf_tx_meta[i]['orig_day'], pdf_tx_meta[i]['orig_time'])
        if key not in p_seen:
            p_seen[key] = len(post_groups)
            post_groups.append({'indices': [i], 'key': key})
        else:
            post_groups[p_seen[key]]['indices'].append(i)

    print(f"Identified {len(post_groups)} post-salary synchronized groups.")
    start_post = datetime.datetime(2026, 8, 25, 11, 30, 0)
    end_post = datetime.datetime(2026, 8, 30, 20, 0, 0)
    post_span = (end_post - start_post).total_seconds()
    step_post = post_span / max(1, len(post_groups))

    prev_post = start_post
    for g_i, g in enumerate(post_groups):
        cur_dt = start_post + datetime.timedelta(seconds=g_i * step_post + ((g_i * 113) % 600))
        if cur_dt.hour < 8:
            cur_dt = cur_dt.replace(hour=8, minute=20 + (g_i * 3 % 35))
        elif cur_dt.hour >= 23:
            cur_dt = cur_dt.replace(hour=21, minute=15 + (g_i * 5 % 30))
        if cur_dt <= prev_post:
            cur_dt = prev_post + datetime.timedelta(minutes=3, seconds=15)
        prev_post = cur_dt

        d_str = f"{cur_dt.day:02d} Aug 2026"
        t_str = f"{cur_dt.strftime('%H:%M:%S')} WIB"
        for idx in g['indices']:
            schedule[idx] = {'date': d_str, 'time': t_str, 'dt': cur_dt}

    # -----------------------------------------------------------------
    # STEP 2: UPDATE EXCEL TEMPLATE (OUTPUT 1)
    # -----------------------------------------------------------------
    print("\n--- STEP 2: POPULATING EXCEL TEMPLATE ---")
    wb = openpyxl.load_workbook(EXCEL_IN)
    ws = wb['Tabel_Mutasi']

    excel_tx_data = []
    active_row_count = 0
    for r in range(6, ws.max_row + 1):
        nom_val = ws.cell(r, 5).value
        # Skip rows with no nominal or nominal == 0 (Rows 16 & 17)
        if nom_val is not None and abs(float(nom_val)) > 0.001:
            idx = active_row_count
            active_row_count += 1
            ws.cell(r, 1).value = active_row_count
            ws.cell(r, 2).value = schedule[idx]['dt'].date()
            ws.cell(r, 3).value = schedule[idx]['time']
            nom_float = float(nom_val)
            ws.cell(r, 6).value = 'CR' if nom_float > 0 else 'DB'

            # Page mapping:
            # Page 1: 10 tx (0..9)
            # Page 2: 12 tx (10..21)
            # Page 3: 12 tx (22..33)
            # Page 4: 12 tx (34..45)
            # Page 5: 12 tx (46..57)
            # Page 6: 12 tx (58..69)
            # Page 7: 5 tx  (70..74)
            if idx < 10:
                p_num, r_idx = 1, idx
            elif idx < 22:
                p_num, r_idx = 2, idx - 10
            elif idx < 34:
                p_num, r_idx = 3, idx - 22
            elif idx < 46:
                p_num, r_idx = 4, idx - 34
            elif idx < 58:
                p_num, r_idx = 5, idx - 46
            elif idx < 70:
                p_num, r_idx = 6, idx - 58
            else:
                p_num, r_idx = 7, idx - 70

            saldo_float = float(ws.cell(r, 7).value) + 0.81
            excel_tx_data.append({
                'no': active_row_count,
                'excel_row': r,
                'page': p_num,
                'row_idx': r_idx,
                'date': schedule[idx]['date'],
                'time': schedule[idx]['time'],
                'nom': nom_float,
                'saldo': saldo_float,
                'saldo_str': format_idr(saldo_float)
            })

    assert active_row_count == 75, f"Expected 75 active rows in Excel, found {active_row_count}"

    # Update Header & Ringkasan sheet
    ws_hr = wb['Header & Ringkasan']
    ws_hr['B10'] = "IBNU AGUN"
    ws_hr['B11'] = "KCP Serang Ciceri"
    ws_hr['B12'] = "01 Aug 2026 - 31 Aug 2026"
    ws_hr['B13'] = datetime.datetime(2026, 11, 12, 0, 0)
    ws_hr['B14'] = "1630016072145"
    ws_hr['B15'] = "IDR"
    ws_hr['B17'] = "AUTO"
    ws_hr['B20'] = "Aug 2026"
    ws_hr['B22'] = 2564938
    ws_hr['B23'] = 8853000
    ws_hr['B24'] = -5308440  # Reconciled value
    ws_hr['B25'] = 6109498
    ws_hr['B26'] = "KLOP"

    wb.save(EXCEL_OUT)
    print(f"Saved populated Excel: {EXCEL_OUT}")

    # -----------------------------------------------------------------
    # STEP 3: HIGH-LEVEL PDF EDITS VIA PDFCRAFT CLIENT
    # -----------------------------------------------------------------
    print("\n--- STEP 3: HIGH-LEVEL PDF EDITS VIA PDFCRAFT CLIENT ---")
    shutil.copyfile(PDF_IN, PDF_OUT)

    with PdfCraftClient() as client:
        doc_id = client.doc_open(PDF_OUT)

        # A. Headers on Pages 1..7
        for p_num in range(1, 8):
            paras = client.get_paragraphs(doc_id, page=p_num)

            # Name
            p_name = [p for p in paras if "ROY DARWIN REZERIUS" in p["text"] and p["rect"][1] < 115]
            if p_name:
                client.edit_text(doc_id, page=p_num, paragraph=p_name[0]["paragraph"], text="IBNU AGUN")
                up = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == p_name[0]["paragraph"]][0]
                dx = VALUE_COL1_X0 - up["rect"][0]
                if abs(dx) > 0.02: client.edit_text(doc_id, page=p_num, paragraph=up["paragraph"], dx=dx)

            # Branch
            paras = client.get_paragraphs(doc_id, page=p_num)
            p_branch = [p for p in paras if "KCP Jakarta Taman Aries" in p["text"] and p["rect"][1] < 135]
            if p_branch:
                client.edit_text(doc_id, page=p_num, paragraph=p_branch[0]["paragraph"], text="KCP Serang Ciceri")
                up = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == p_branch[0]["paragraph"]][0]
                dx = VALUE_COL1_X0 - up["rect"][0]
                if abs(dx) > 0.02: client.edit_text(doc_id, page=p_num, paragraph=up["paragraph"], dx=dx)

            # Period
            paras = client.get_paragraphs(doc_id, page=p_num)
            p_per = [p for p in paras if "01 Apr 2026 - 30 Apr 2026" in p["text"] and p["rect"][1] < 115]
            if p_per:
                client.edit_text(doc_id, page=p_num, paragraph=p_per[0]["paragraph"], text="01 Aug 2026 - 31 Aug 2026")
                up = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == p_per[0]["paragraph"]][0]
                dx = VALUE_COL2_X0 - up["rect"][0]
                if abs(dx) > 0.02: client.edit_text(doc_id, page=p_num, paragraph=up["paragraph"], dx=dx)

            # Issued on (Template matches 12 Nov 2026)
            paras = client.get_paragraphs(doc_id, page=p_num)
            p_iss = [p for p in paras if "09 Sep 2026" in p["text"] and p["rect"][1] < 135]
            if p_iss:
                client.edit_text(doc_id, page=p_num, paragraph=p_iss[0]["paragraph"], text="12 Nov 2026")
                up = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == p_iss[0]["paragraph"]][0]
                dx = VALUE_COL2_X0 - up["rect"][0]
                if abs(dx) > 0.02: client.edit_text(doc_id, page=p_num, paragraph=up["paragraph"], dx=dx)

        # B. Page 1 Account Number & Tabungan NOW IDR
        paras = client.get_paragraphs(doc_id, page=1)
        p_acc = [p for p in paras if "1650003584860" in p["text"]]
        if p_acc:
            client.edit_text(doc_id, page=1, paragraph=p_acc[0]["paragraph"], text="1630016072145")
            up = [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == p_acc[0]["paragraph"]][0]
            dx = VALUE_ACC_X0 - up["rect"][0]
            if abs(dx) > 0.02: client.edit_text(doc_id, page=1, paragraph=up["paragraph"], dx=dx)

        # C. Update Dates & Times across all pages (1..7)
        for p_num in range(1, 8):
            paras = client.get_paragraphs(doc_id, page=p_num)
            min_top = 310 if p_num == 1 else 180
            t_paras = [p for p in paras if min_top <= p["rect"][1] <= 780]
            wib_paras = sorted([p for p in t_paras if "WIB" in p["text"]], key=lambda x: x["rect"][1])

            page_txs = [tx for tx in excel_tx_data if tx['page'] == p_num]
            assert len(wib_paras) == len(page_txs), f"Page {p_num}: wib count {len(wib_paras)} != tx count {len(page_txs)}"

            for r_i, tx in enumerate(page_txs):
                target_wib = wib_paras[r_i]
                y_anchor = target_wib["rect"][1]

                # Update Time
                client.edit_text(doc_id, page=p_num, paragraph=target_wib["paragraph"], text=tx['time'])
                up_t = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == target_wib["paragraph"]][0]
                dx_t = COL_DATE_TIME_X0 - up_t["rect"][0]
                if abs(dx_t) > 0.02: client.edit_text(doc_id, page=p_num, paragraph=up_t["paragraph"], dx=dx_t)

                # Update Date
                d_paras = [p for p in t_paras if 0 < (y_anchor - p["rect"][1]) < 18 and 45 <= p["rect"][0] <= 95]
                if d_paras:
                    client.edit_text(doc_id, page=p_num, paragraph=d_paras[0]["paragraph"], text=tx['date'])
                    up_d = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == d_paras[0]["paragraph"]][0]
                    dx_d = COL_DATE_TIME_X0 - up_d["rect"][0]
                    if abs(dx_d) > 0.02: client.edit_text(doc_id, page=p_num, paragraph=up_d["paragraph"], dx=dx_d)

        # D. Update the 6 changed Nominals (Tx 10, 21, 23, 24, 60, 75)
        changed_tx_nos = [10, 21, 23, 24, 60, 75]
        for tx in excel_tx_data:
            if tx['no'] in changed_tx_nos:
                p_num = tx['page']
                paras = client.get_paragraphs(doc_id, page=p_num)
                min_top = 310 if p_num == 1 else 180
                t_paras = [p for p in paras if min_top <= p["rect"][1] <= 780]
                wib_paras = sorted([p for p in t_paras if "WIB" in p["text"]], key=lambda x: x["rect"][1])
                target_wib = wib_paras[tx['row_idx']]
                y_anchor = target_wib["rect"][1]

                nom_paras = [p for p in t_paras if abs(p["rect"][1] - y_anchor) < 15 and 360 <= p["rect"][0] <= 450 and ("+" in p["text"] or "-" in p["text"])]
                assert nom_paras, f"Nominal para not found for Tx {tx['no']}"
                nom_str = f"+ {format_idr(tx['nom'])}" if tx['nom'] > 0 else f"- {format_idr(tx['nom'])}"
                nom_col = COLOR_CREDIT_GREEN if tx['nom'] > 0 else COLOR_DEBIT_BLACK
                client.edit_text(doc_id, page=p_num, paragraph=nom_paras[0]["paragraph"], text=nom_str, color=nom_col)
                up_nom = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == nom_paras[0]["paragraph"]][0]
                dx_nom = COL_NOMINAL_RIGHT_X - up_nom["rect"][2]
                if abs(dx_nom) > 0.02: client.edit_text(doc_id, page=p_num, paragraph=up_nom["paragraph"], dx=dx_nom)

        client.doc_save(doc_id, PDF_OUT)
        client.doc_close(doc_id)
        print(f"PdfCraft high-level edits completed: {PDF_OUT}")

    # -----------------------------------------------------------------
    # STEP 4: STREAM-LEVEL PRECISION RECONSTRUCTION
    # -----------------------------------------------------------------
    print("\n--- STEP 4: STREAM-LEVEL RECONSTRUCTION (SUMMARY BOX, NO/SALDO, PAGE NUMS) ---")
    patch_streams_perfect(PDF_OUT, excel_tx_data)

def patch_streams_perfect(pdf_path, excel_tx_data):
    with open(pdf_path, 'rb') as f:
        pdf_bytes = f.read()

    # 1. Parse XRef stream
    sx_matches = re.findall(rb'startxref[\r\n]+(\d+)', pdf_bytes)
    xref_offset = int(sx_matches[-1])

    m_xref = re.search(rb'\b(\d+)\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes[xref_offset-50:], re.DOTALL)
    xref_oid = int(m_xref.group(1))
    xref_dict = m_xref.group(2)
    xref_stream = m_xref.group(3)

    xref_start_pos = re.search(rb'\b' + str(xref_oid).encode() + rb'\s+0\s+obj\b', pdf_bytes).start()

    m_size = re.search(r'/Size\s+(\d+)', xref_dict.decode('latin1'))
    size = int(m_size.group(1))
    m_w = re.search(r'/W\s*\[\s*(\d+)\s+(\d+)\s+(\d+)\s*\]', xref_dict.decode('latin1'))
    w1, w2, w3 = int(m_w.group(1)), int(m_w.group(2)), int(m_w.group(3))
    cols = w1 + w2 + w3
    stride = cols + 1
    decomp_xref = zlib.decompress(xref_stream)

    rows = []
    prev = bytearray(cols)
    for i in range(size):
        row_bytes = decomp_xref[i*stride : (i+1)*stride]
        filter_type = row_bytes[0]
        curr = bytearray(row_bytes[1:])
        if filter_type == 2:
            for c in range(cols):
                curr[c] = (curr[c] + prev[c]) % 256
        prev = curr
        f1 = curr[0] if w1 == 1 else 0
        f2 = (curr[w1] << 8) | curr[w1+1] if w2 == 2 else curr[w1]
        f3 = (curr[w1+w2] << 8) | curr[w1+w2+1] if w3 == 2 else curr[w1+w2]
        rows.append([f1, f2, f3])

    top_objs = [i for i in range(size) if rows[i][0] == 1 and i != xref_oid]
    top_objs.sort(key=lambda oid: rows[oid][1])

    header = pdf_bytes[:rows[top_objs[0]][1]]
    obj_raw = {}
    for i, oid in enumerate(top_objs):
        start_idx = rows[oid][1]
        end_idx = rows[top_objs[i+1]][1] if i + 1 < len(top_objs) else xref_start_pos
        obj_raw[oid] = pdf_bytes[start_idx:end_idx]

    # Authentic character widths from 0.pdf:
    # Regular 8pt:
    reg_w = {
        '1': 2.6796875, '2': 4.51953125, '3': 4.5625, '4': 4.4375, '5': 4.640625,
        '6': 4.640625, '7': 4.12109375, '8': 4.71875, '9': 4.640625, '0': 5.359375,
        ' ': 1.76171875, 'd': 4.71875, 'a': 4.16015625, 'r': 2.83984375, 'i': 1.71875,
        'o': 4.5625, 'f': 2.6796875
    }
    # Bold 8pt:
    bold_w = {
        '1': 3.16015625, '2': 4.76171875, '3': 4.83984375, '4': 4.87890625, '5': 4.83984375,
        '6': 4.87890625, '7': 4.3203125, '8': 4.9609375, '9': 4.87890625, '0': 5.4375,
        '.': 1.83984375, ',': 1.83984375, ' ': 1.83984375, 'd': 4.9609375, 'a': 4.4375,
        'r': 3.23828125, 'i': 2.078125, 'o': 4.71875, 'f': 2.6796875
    }

    def get_reg_width(s):
        return sum(reg_w.get(c, 4.0) for c in s)

    def get_bold_width(s):
        return sum(bold_w.get(c, 4.8) for c in s)

    # Identify Page Content streams
    # They contain the saldo color definition in PDF_OUT
    page_content_list = []
    for oid in top_objs:
        raw = obj_raw[oid]
        m_s = re.search(rb'stream[\r\n]+(.*?)[\r\n]+endstream', raw, re.DOTALL)
        if m_s:
            try:
                dec = zlib.decompress(m_s.group(1))
                if b"0.07451 0.294118 0.729412 rg/R2 8 Tf" in dec:
                    page_content_list.append(oid)
            except:
                pass

    print(f"Discovered Page Content OIDs: {page_content_list}")
    assert len(page_content_list) == 7, f"Expected 7 pages mapped, got {len(page_content_list)}"
    page_content_oids = {p_idx + 1: oid for p_idx, oid in enumerate(page_content_list)}

    # -------------------------------------------------------------
    # 4A. PATCH SUMMARY BOX ON PAGE 1
    # -------------------------------------------------------------
    p1_oid = page_content_oids[1]
    raw1 = obj_raw[p1_oid]
    m_s1 = re.search(rb'stream[\r\n]+(.*?)[\r\n]+endstream', raw1, re.DOTALL)
    stext = zlib.decompress(m_s1.group(1)).decode('latin1', errors='ignore')

    # Find Block 1 (Colons & Labels)
    pos_c1 = stext.find('446.12 667')
    start_b1 = stext.rfind('q', 0, pos_c1)
    pos_c4 = stext.find('446.12 597')
    m_end_b1 = re.search(r'ET\s*Q', stext[pos_c4:])
    assert m_end_b1, "End of B1 not found"
    end_b1 = pos_c4 + m_end_b1.end()

    # Find Block 2 (Values)
    pos_now = stext.find('16 676 cm')
    end_b2 = stext.rfind('q', 0, pos_now)
    matches_b2 = list(re.finditer(r'q\s+1\s+0\s+0\s+1\s+[\d\.]+\s+667\s+cm', stext[end_b1:end_b2]))
    if not matches_b2:
        matches_b2 = list(re.finditer(r'q\s+1\s+0\s+0\s+1\s+0\s+0\s+cm', stext[end_b1:end_b2]))
    assert matches_b2, "Value start not found"
    start_b2 = end_b1 + matches_b2[-1].start()

    # Clean Block 1: 8 independent BT blocks, '/' in /R2 Bold!
    new_b1 = f"""q 1 0 0 1 0 0 cm
BT
1 0 0 1 446.12 667 Tm
/R1 8 Tf
0.38039 0.35294 0.35294 rg
<{to_hex(':')}> Tj
0 g
ET
BT
1 0 0 1 298 667 Tm
/R2 8 Tf
0.10196 0.10196 0.10196 rg
<{to_hex('Saldo Awal/')}> Tj
0 g
/R3 8 Tf
0.10196 0.10196 0.10196 rg
<{to_hex('Initial Balance')}> Tj
0 g
ET
BT
1 0 0 1 298 644 Tm
/R2 8 Tf
0.10196 0.10196 0.10196 rg
<{to_hex('Dana Masuk/')}> Tj
0 g
/R3 8 Tf
0.10196 0.10196 0.10196 rg
<{to_hex('Incoming Transactions')}> Tj
0 g
ET
BT
1 0 0 1 446.12 644 Tm
/R1 8 Tf
0.02353 0.66667 0.43529 rg
<{to_hex(':')}> Tj
0 g
ET
BT
1 0 0 1 298 621 Tm
/R2 8 Tf
0.10196 0.10196 0.10196 rg
<{to_hex('Dana Keluar/')}> Tj
0 g
/R3 8 Tf
0.10196 0.10196 0.10196 rg
<{to_hex('Outgoing Transactions')}> Tj
0 g
ET
BT
1 0 0 1 446.12 621 Tm
/R1 8 Tf
0.10196 0.10196 0.10196 rg
<{to_hex(':')}> Tj
0 g
ET
BT
1 0 0 1 298 597 Tm
/R2 8 Tf
0.10196 0.10196 0.10196 rg
<{to_hex('Saldo Akhir/')}> Tj
0 g
/R3 8 Tf
0.10196 0.10196 0.10196 rg
<{to_hex('Closing Balance')}> Tj
0 g
ET
BT
1 0 0 1 446.12 597 Tm
/R1 8 Tf
0.38039 0.35294 0.35294 rg
<{to_hex(':')}> Tj
0 g
ET
Q"""

    # Clean Block 2: 4 independent BT blocks for values, exact right alignment at 567.00 pt!
    new_b2 = f"""q 1 0 0 1 0 0 cm
BT
1 0 0 1 519.32 667 Tm
/R2 8 Tf
0.38039 0.35294 0.35294 rg
<{to_hex('2.564.938,81')}> Tj
0 g
ET
BT
1 0 0 1 508.45 644 Tm
/R2 8 Tf
0.02353 0.66667 0.43529 rg
<{to_hex('+ 8.853.000,00')}> Tj
0 g
ET
BT
1 0 0 1 510.25 621 Tm
/R2 8 Tf
0.10196 0.10196 0.10196 rg
<{to_hex('- 5.308.440,00')}> Tj
0 g
ET
BT
1 0 0 1 520.29 597 Tm
/R2 8 Tf
0.07451 0.29412 0.72941 rg
<{to_hex('6.109.498,81')}> Tj
0 g
ET
Q """

    stext = stext[:start_b2] + new_b2 + stext[end_b2:]
    stext = stext[:start_b1] + new_b1 + stext[end_b1:]

    # Put modified stext back as bytearray for subsequent row & page num patching on page 1
    p1_decomp = stext.encode('latin1')

    # -------------------------------------------------------------
    # 4B. PATCH NO, SALDO, AND PAGE NUMBERS ACROSS PAGES 1..7
    # -------------------------------------------------------------
    row_pattern = re.compile(
        rb'(q\s+1\s+0\s+0\s+1\s+(?:19\.\d+|20(?:\.0+)?)\s+([\d\.]+)\s+cm\s+BT\s+0\s+0\s+0\s+rg/R1\s+8\s+Tf(/R\d+\s+gs).*?0\.07451\s+0\.294118\s+0\.729412\s+rg/R2\s+8\s+Tf.*?ET\s+Q)',
        re.DOTALL
    )

    PAGE_RIGHT_X = 563.80

    for p_num in range(1, 8):
        oid = page_content_oids[p_num]
        p_txs = [t for t in excel_tx_data if t["page"] == p_num]

        if p_num == 1:
            decomp = p1_decomp
        else:
            raw = obj_raw[oid]
            m_s = re.search(rb'stream[\r\n]+(.*?)[\r\n]+endstream', raw, re.DOTALL)
            decomp = zlib.decompress(m_s.group(1))

        # 1. Patch No & Saldo rows
        matches = list(row_pattern.finditer(decomp))
        assert len(matches) == len(p_txs), f"Page {p_num}: expected {len(p_txs)} rows, found {len(matches)}"

        for i in reversed(range(len(matches))):
            m = matches[i]
            tx = p_txs[i]
            y_str = m.group(2)
            gs_str = m.group(3)

            no_str = str(tx["no"])
            sal_str = tx["saldo_str"]

            w_no = get_reg_width(no_str)
            w_sal = get_bold_width(sal_str)

            # Target right edge: 571.00 pt
            # x_start: 19.929 on page 1, 20.00 on pages 2..7
            x_start_val = 19.929 if p_num == 1 else 20.00
            dist = 571.00 - x_start_val - w_no - w_sal
            calc_k = - round(dist / 0.008)

            no_u16 = to_utf16_be(no_str)
            sal_u16 = to_utf16_be(sal_str)

            x_str = b"19.929" if p_num == 1 else b"20"
            repl = (
                b"q 1 0 0 1 " + x_str + b" " + y_str + b" cm BT 0 0 0 rg/R1 8 Tf" + gs_str +
                b"(" + no_u16 + b") Tj 0.07451 0.294118 0.729412 rg/R2 8 Tf[ " +
                str(calc_k).encode() + b"(" + sal_u16 + b")]TJ ET Q"
            )
            decomp = decomp[:m.start()] + repl + decomp[m.end():]

        # 2. Patch Page Numbers (Bold 'P dari 7' and Italic 'P of 7')
        s_bold = f"{p_num} dari 7"
        w_b = get_bold_width(s_bold)
        x_b = PAGE_RIGHT_X - w_b

        s_it = f"{p_num} of 7"
        w_it = get_reg_width(s_it)
        x_it = PAGE_RIGHT_X - w_it

        page_num_replacements = []

        # Italic block: q 1 0 0 1 <x> 726 cm BT 0 0 0 rg/R3 8 Tf/<gs> gs... ET Q
        m_it = re.search(rb'q\s+1\s+0\s+0\s+1\s+[\d\.]+\s+726\s+cm\s+BT\s+0\s+0\s+0\s+rg/R3\s+8\s+Tf(/R\d+\s+gs).*?ET\s+Q', decomp, re.DOTALL)
        assert m_it is not None, f"Page {p_num}: italic page number block not found"
        gs_it = m_it.group(1)
        new_it = (
            f"q 1 0 0 1 {x_it:.2f} 726 cm BT 0 0 0 rg/R1 8 Tf 1 0 0.2 1 0 0 Tm".encode() +
            gs_it + b"(" + to_utf16_be(s_it) + b") Tj ET Q"
        )
        page_num_replacements.append((m_it.start(), m_it.end(), new_it))

        # Bold blocks at y=736
        bold_blocks = list(re.finditer(rb'q\s+1\s+0\s+0\s+1\s+[\d\.]+\s+736\s+cm\s+BT\s+0\s+0\s+0\s+rg/R2\s+8\s+Tf(/R\d+\s+gs).*?ET\s+Q', decomp, re.DOTALL))
        if bold_blocks:
            gs_b = bold_blocks[-1].group(1)
            new_b = (
                f"q 1 0 0 1 {x_b:.2f} 736 cm BT 0 0 0 rg/R2 8 Tf".encode() +
                gs_b + b"(" + to_utf16_be(s_bold) + b") Tj ET Q"
            )
            page_num_replacements.append((bold_blocks[0].start(), bold_blocks[0].end(), new_b))
            for extra_bb in bold_blocks[1:]:
                page_num_replacements.append((extra_bb.start(), extra_bb.end(), b""))

        page_num_replacements.sort(key=lambda x: x[0], reverse=True)
        for s_pos, e_pos, r_bytes in page_num_replacements:
            decomp = decomp[:s_pos] + r_bytes + decomp[e_pos:]

        # Compress and update obj_raw[oid]
        new_comp = zlib.compress(decomp, 9)
        raw_obj = obj_raw[oid]
        m_stream = re.search(rb'stream[\r\n]+(.*?)[\r\n]+endstream', raw_obj, re.DOTALL)
        before_s = raw_obj[:m_stream.start()]
        new_before_s = re.sub(rb'/Length\s+\d+', f'/Length {len(new_comp)}'.encode(), before_s)
        after_s = raw_obj[m_stream.end():]
        obj_raw[oid] = new_before_s + b"stream\n" + new_comp + b"\nendstream" + after_s
        print(f"Patched Page {p_num} (OID {oid}): {len(p_txs)} rows + Page Numbers ({s_bold} / {s_it})")

    # -------------------------------------------------------------
    # 4C. REASSEMBLE PDF & RECALCULATE XREF STREAM
    # -------------------------------------------------------------
    out = bytearray(header)
    for oid in top_objs:
        new_offset = len(out)
        rows[oid][1] = new_offset
        out.extend(obj_raw[oid])

    xref_start = len(out)
    rows[xref_oid][1] = xref_start

    new_xref_uncompressed = bytearray()
    for r in rows:
        new_xref_uncompressed.append(0)  # Filter None
        new_xref_uncompressed.append(r[0])
        new_xref_uncompressed.append((r[1] >> 8) & 0xFF)
        new_xref_uncompressed.append(r[1] & 0xFF)
        new_xref_uncompressed.append((r[2] >> 8) & 0xFF)
        new_xref_uncompressed.append(r[2] & 0xFF)

    comp_xref = zlib.compress(bytes(new_xref_uncompressed), 9)
    new_xref_dict = re.sub(rb'/Length\s+\d+', f'/Length {len(comp_xref)}'.encode(), xref_dict)

    xref_obj_str = (
        f"{xref_oid} 0 obj\n<<".encode() + new_xref_dict + b'>>\nstream\n' +
        comp_xref + b'\nendstream\nendobj\nstartxref\n' + str(xref_start).encode() + b'\n%%EOF\n'
    )
    out.extend(xref_obj_str)

    with open(pdf_path, 'wb') as f:
        f.write(out)
    print(f"\nFinal PDF perfectly reassembled: {pdf_path} ({len(out)} bytes)")

if __name__ == "__main__":
    run()
