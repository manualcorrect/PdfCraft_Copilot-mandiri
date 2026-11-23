"""
Unified Production Builder for Bank Mandiri e-Statement:
Client: KEISYA AULIA
Period: September 2026 (01 Sep 2026 - 30 Sep 2026)
Target Folder: D:\\X_Files\\rekening\\PT BENDI NASHA NIAGA INDUSTRI\\keisya\\Folder Baru\\sep

Outputs:
- Template_Mutasi_SEP_OUTPUT_1.xlsx
- REK_KEISYA_SEP_OUTPUT_1.pdf

Adheres strictly to Mandiri Ground Truth Specifications:
1. Keterangan 100% UNTOUCHED (zero shift, zero re-typesetting).
2. Dates & Times synchronized chronologically across September 2026.
3. Column sequence numbers (No) 1..50 automatically populated.
4. Issued on / Dicetak pada matches template (12 Nov 2026).
5. Page numbers: P dari 5 / P of 5 with authentic Mandiri TTInterphases oblique.
6. Saldos anchored at exact right edge 571.00 pt.
7. Balance 100% klop (2.698.988,81 + 11.379.332,00 - 7.227.500,00 = 6.850.820,81).
"""

import os
import sys
import shutil
import re
import zlib
import io
import datetime
import openpyxl
import pdfplumber
import pypdfium2 as pdfium
from fontTools.ttLib import TTFont

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

BASE_DIR = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep"
EXCEL_IN = os.path.join(BASE_DIR, "Template_Mutasi_SEP.xlsx")
PDF_IN = os.path.join(BASE_DIR, "0.pdf")

WORKSPACE_OUT = r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output"
os.makedirs(WORKSPACE_OUT, exist_ok=True)
EXCEL_OUT = os.path.join(WORKSPACE_OUT, "Template_Mutasi_SEP_OUTPUT_1.xlsx")
PDF_OUT = os.path.join(WORKSPACE_OUT, "REK_KEISYA_SEP_OUTPUT_1.pdf")

def format_idr(num: float) -> str:
    return f"{abs(num):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def to_utf16_be(s: str) -> bytes:
    return s.encode("utf-16-be")

def run_build():
    print("=================================================================")
    print("STARTING UNIFIED BUILD: KEISYA AULIA - SEPTEMBER 2026 (OUTPUT 1)")
    print("=================================================================")
    
    # -----------------------------------------------------------------
    # STEP 1: EXTRACT TIMESTAMPS & GENERATE SYNCHRONIZED SCHEDULE
    # -----------------------------------------------------------------
    print("\n--- STEP 1: GENERATING SYNCHRONIZED CHRONOLOGICAL SCHEDULE ---")
    pdf_tx_meta = []
    with pdfplumber.open(PDF_IN) as pdf:
        for p_idx, page in enumerate(pdf.pages):
            words = page.extract_words()
            min_top = 320 if p_idx == 0 else 200
            table_words = [w for w in words if min_top <= w['top'] <= 800]
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

    assert len(pdf_tx_meta) == 50, f"Expected 50 tx in 0.pdf, found {len(pdf_tx_meta)}"
    print(f"Extracted {len(pdf_tx_meta)} transaction metadata entries from 0.pdf.")

    sal_idx = 36  # Tx 37 in 1-based indexing (Salary)
    schedule = [None] * 50

    # Pre-salary groups (Tx 1..36)
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
    start_pre = datetime.datetime(2026, 9, 1, 9, 0, 0)
    end_pre = datetime.datetime(2026, 9, 24, 18, 0, 0)
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
        
        d_str = f"{cur_dt.day:02d} Sep 2026"
        t_str = f"{cur_dt.strftime('%H:%M:%S')} WIB"
        for idx in g['indices']:
            schedule[idx] = {'date': d_str, 'time': t_str, 'dt': cur_dt}

    # Salary Tx 37
    schedule[sal_idx] = {
        'date': '25 Sep 2026',
        'time': '04:00:00 WIB',
        'dt': datetime.datetime(2026, 9, 25, 4, 0, 0)
    }

    # Closing Fee Tx 50
    schedule[49] = {
        'date': '30 Sep 2026',
        'time': '23:59:00 WIB',
        'dt': datetime.datetime(2026, 9, 30, 23, 59, 0)
    }

    # Post-salary intermediate groups (Tx 38..49)
    post_groups = []
    p_seen = {}
    for i in range(sal_idx + 1, 49):
        key = (pdf_tx_meta[i]['orig_day'], pdf_tx_meta[i]['orig_time'])
        if key not in p_seen:
            p_seen[key] = len(post_groups)
            post_groups.append({'indices': [i], 'key': key})
        else:
            post_groups[p_seen[key]]['indices'].append(i)

    print(f"Identified {len(post_groups)} post-salary synchronized groups.")
    start_post = datetime.datetime(2026, 9, 25, 11, 30, 0)
    end_post = datetime.datetime(2026, 9, 30, 20, 0, 0)
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
        
        d_str = f"{cur_dt.day:02d} Sep 2026"
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
    for r in range(6, 60):
        nom_val = ws.cell(r, 5).value
        if nom_val is not None and abs(float(nom_val)) > 0.001:
            idx = active_row_count
            active_row_count += 1
            ws.cell(r, 1).value = active_row_count
            ws.cell(r, 2).value = schedule[idx]['dt'].date()
            ws.cell(r, 3).value = schedule[idx]['time']
            nom_float = float(nom_val)
            ws.cell(r, 6).value = 'CR' if nom_float > 0 else 'DB'
            
            # Map page and row_idx
            if idx < 10:
                p_num, r_idx = 1, idx
            elif idx < 22:
                p_num, r_idx = 2, idx - 10
            elif idx < 34:
                p_num, r_idx = 3, idx - 22
            elif idx < 46:
                p_num, r_idx = 4, idx - 34
            else:
                p_num, r_idx = 5, idx - 46
                
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

    assert active_row_count == 50, f"Expected 50 active rows in Excel, found {active_row_count}"
    wb.save(EXCEL_OUT)
    print(f"Saved populated Excel: {EXCEL_OUT}")

    # -----------------------------------------------------------------
    # STEP 3: HIGH-LEVEL PDF EDITS (PDFCRAFT CLIENT)
    # -----------------------------------------------------------------
    print("\n--- STEP 3: HIGH-LEVEL PDF EDITS VIA PDFCRAFT CLIENT ---")
    shutil.copyfile(PDF_IN, PDF_OUT)

    with PdfCraftClient() as client:
        doc_id = client.doc_open(PDF_OUT)
        
        # A. Headers on Pages 1..5
        for p_num in range(1, 6):
            paras = client.get_paragraphs(doc_id, page=p_num)
            
            # Name
            p_name = [p for p in paras if "ROY DARWIN REZERIUS" in p["text"] and p["rect"][1] < 115]
            if p_name:
                client.edit_text(doc_id, page=p_num, paragraph=p_name[0]["paragraph"], text="KEISYA AULIA")
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
            p_per = [p for p in paras if "01 Mar 2026 - 31 Mar 2026" in p["text"] and p["rect"][1] < 115]
            if p_per:
                client.edit_text(doc_id, page=p_num, paragraph=p_per[0]["paragraph"], text="01 Sep 2026 - 30 Sep 2026")
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

        # B. Page 1 Summary Box & Account Number
        paras = client.get_paragraphs(doc_id, page=1)
        
        # Account Number
        p_acc = [p for p in paras if "1650003584860" in p["text"]]
        if p_acc:
            client.edit_text(doc_id, page=1, paragraph=p_acc[0]["paragraph"], text="1630016478664")
            up = [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == p_acc[0]["paragraph"]][0]
            dx = VALUE_ACC_X0 - up["rect"][0]
            if abs(dx) > 0.02: client.edit_text(doc_id, page=1, paragraph=up["paragraph"], dx=dx)

        # Saldo Awal (2.698.988,81)
        paras = client.get_paragraphs(doc_id, page=1)
        p_sawal = [p for p in paras if 160 <= p["rect"][1] <= 180 and p["rect"][0] > 480][0]
        client.edit_text(doc_id, page=1, paragraph=p_sawal["paragraph"], text="2.698.988,81", color=COLOR_SALDO_AWAL_GRAY)
        up = [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == p_sawal["paragraph"]][0]
        dx = SUMMARY_RIGHT_X - up["rect"][2]
        if abs(dx) > 0.01: client.edit_text(doc_id, page=1, paragraph=up["paragraph"], dx=dx)

        # Dana Masuk (+ 11.379.332,00)
        paras = client.get_paragraphs(doc_id, page=1)
        p_dmasuk = [p for p in paras if 185 <= p["rect"][1] <= 205 and p["rect"][0] > 480][0]
        client.edit_text(doc_id, page=1, paragraph=p_dmasuk["paragraph"], text="+ 11.379.332,00", color=COLOR_CREDIT_GREEN)
        up = [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == p_dmasuk["paragraph"]][0]
        dx = SUMMARY_RIGHT_X - up["rect"][2]
        if abs(dx) > 0.01: client.edit_text(doc_id, page=1, paragraph=up["paragraph"], dx=dx)

        # Dana Keluar (- 7.227.500,00)
        paras = client.get_paragraphs(doc_id, page=1)
        p_dkeluar = [p for p in paras if 208 <= p["rect"][1] <= 228 and p["rect"][0] > 480][0]
        client.edit_text(doc_id, page=1, paragraph=p_dkeluar["paragraph"], text="- 7.227.500,00", color=COLOR_DEBIT_BLACK)
        up = [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == p_dkeluar["paragraph"]][0]
        dx = SUMMARY_RIGHT_X - up["rect"][2]
        if abs(dx) > 0.01: client.edit_text(doc_id, page=1, paragraph=up["paragraph"], dx=dx)

        # Saldo Akhir (6.850.820,81)
        paras = client.get_paragraphs(doc_id, page=1)
        p_sakhir = [p for p in paras if 230 <= p["rect"][1] <= 255 and p["rect"][0] > 480][0]
        client.edit_text(doc_id, page=1, paragraph=p_sakhir["paragraph"], text="6.850.820,81", color=COLOR_RUNNING_SALDO_BLUE)
        up = [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == p_sakhir["paragraph"]][0]
        dx = SUMMARY_RIGHT_X - up["rect"][2]
        if abs(dx) > 0.01: client.edit_text(doc_id, page=1, paragraph=up["paragraph"], dx=dx)

        # C. Update Dates, Times, and Changed Nominals across all pages
        for page_num in range(1, 6):
            page_txs = [t for t in excel_tx_data if t["page"] == page_num]
            base_y = 343.92 if page_num == 1 else 227.92
            
            for tx in page_txs:
                row_y = base_y + tx["row_idx"] * 46.00
                
                # 1. Update Date
                paras = client.get_paragraphs(doc_id, page=page_num)
                p_date = [p for p in paras if abs(p["rect"][1] - (row_y - 4.0)) < 10 and 45 <= p["rect"][0] <= 85 and "WIB" not in p["text"]]
                if p_date:
                    client.edit_text(doc_id, page=page_num, paragraph=p_date[0]["paragraph"], text=tx["date"])
                    up_d = [p for p in client.get_paragraphs(doc_id, page=page_num) if p["paragraph"] == p_date[0]["paragraph"]][0]
                    dx_d = COL_DATE_TIME_X0 - up_d["rect"][0]
                    if abs(dx_d) > 0.02: client.edit_text(doc_id, page=page_num, paragraph=up_d["paragraph"], dx=dx_d)
                    
                # 2. Update Time
                paras = client.get_paragraphs(doc_id, page=page_num)
                p_time = [p for p in paras if abs(p["rect"][1] - (row_y + 5.0)) < 10 and 45 <= p["rect"][0] <= 85 and "WIB" in p["text"]]
                if p_time:
                    client.edit_text(doc_id, page=page_num, paragraph=p_time[0]["paragraph"], text=tx["time"])
                    up_t = [p for p in client.get_paragraphs(doc_id, page=page_num) if p["paragraph"] == p_time[0]["paragraph"]][0]
                    dx_t = COL_DATE_TIME_X0 - up_t["rect"][0]
                    if abs(dx_t) > 0.02: client.edit_text(doc_id, page=page_num, paragraph=up_t["paragraph"], dx=dx_t)

                # 3. Update Changed Nominals: Tx 10 (-181.000,00), Tx 37 (+6.778.332,00), Tx 50 (-5.000,00)
                if tx["no"] in [10, 37, 50]:
                    paras = client.get_paragraphs(doc_id, page=page_num)
                    p_nom = [p for p in paras if abs(p["rect"][1] - row_y) < 15 and 370 <= p["rect"][0] <= 450]
                    if p_nom:
                        is_credit = tx["nom"] > 0
                        nom_str = ("+" if is_credit else "-") + format_idr(tx["nom"])
                        col = COLOR_CREDIT_GREEN if is_credit else COLOR_DEBIT_BLACK
                        client.edit_text(doc_id, page=page_num, paragraph=p_nom[0]["paragraph"], text=nom_str, color=col)
                        up_n = [p for p in client.get_paragraphs(doc_id, page=page_num) if p["paragraph"] == p_nom[0]["paragraph"]][0]
                        dx_n = COL_NOMINAL_RIGHT_X - up_n["rect"][2]
                        if abs(dx_n) > 0.01: client.edit_text(doc_id, page=page_num, paragraph=up_n["paragraph"], dx=dx_n)

        client.doc_save(doc_id)
        print("Completed Step 3: High-level edits saved cleanly.")

    # -----------------------------------------------------------------
    # STEP 4: BINARY STREAM PATCHING (SALDOS, NO, PAGE NUMBERS)
    # -----------------------------------------------------------------
    print("\n--- STEP 4: BINARY STREAM PATCHING & XREF REGENERATION ---")
    with open(PDF_OUT, "rb") as f:
        pdf_bytes = f.read()

    # Parse XRef stream in PDF_OUT
    m_startxref = re.search(rb'startxref\s+(\d+)', pdf_bytes)
    startxref = int(m_startxref.group(1))
    
    # Locate XRef stream object
    m_xref = re.search(rb'(\d+)\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes[startxref-200:])
    xref_oid = int(m_xref.group(1))
    xref_dict = m_xref.group(2)
    xref_stream = m_xref.group(3)
    xref_decomp = zlib.decompress(xref_stream)

    cols = 5
    stride = cols + 1
    total_objects = len(xref_decomp) // stride
    rows = []
    prev = bytearray(cols)
    for i in range(total_objects):
        row_bytes = xref_decomp[i*stride : (i+1)*stride]
        filter_type = row_bytes[0]
        curr = bytearray(row_bytes[1:])
        if filter_type == 2:
            for c in range(cols):
                curr[c] = (curr[c] + prev[c]) % 256
        prev = curr
        f1 = curr[0]
        f2 = (curr[1] << 8) | curr[2]
        f3 = (curr[3] << 8) | curr[4]
        rows.append([f1, f2, f3])

    # Find top-level objects
    top_matches = list(re.finditer(rb'(\d+)\s+0\s+obj\b', pdf_bytes))
    top_objs = [int(m.group(1)) for m in top_matches if int(m.group(1)) != xref_oid]
    
    first_oid = top_objs[0]
    header_end = pdf_bytes.find(str(first_oid).encode() + b" 0 obj")
    header = pdf_bytes[:header_end]

    obj_raw = {}
    for i in range(len(top_objs)):
        oid = top_objs[i]
        start_idx = top_matches[i].start()
        end_idx = top_matches[i+1].start() if i + 1 < len(top_objs) else pdf_bytes.find(str(xref_oid).encode() + b" 0 obj")
        obj_raw[oid] = pdf_bytes[start_idx:end_idx]

    # Load authentic font metrics from 0.pdf
    with open(PDF_IN, "rb") as f0:
        b0 = f0.read()
        ttf_reg = TTFont(io.BytesIO(zlib.decompress(re.search(rb'\b394\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', b0, re.DOTALL).group(2))))
        ttf_bold = TTFont(io.BytesIO(zlib.decompress(re.search(rb'\b397\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', b0, re.DOTALL).group(2))))
        map_reg = zlib.decompress(re.search(rb'\b393\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', b0, re.DOTALL).group(2))
        map_bold = zlib.decompress(re.search(rb'\b396\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', b0, re.DOTALL).group(2))

    hmtx_reg = ttf_reg['hmtx']
    units_reg = ttf_reg['head'].unitsPerEm
    hmtx_bold = ttf_bold['hmtx']
    units_bold = ttf_bold['head'].unitsPerEm

    def get_no_width(s):
        w = 0.0
        for ch in s:
            cid = ord(ch)
            gid = (map_reg[cid*2] << 8) | map_reg[cid*2 + 1]
            adv = hmtx_reg[f"glyph{gid:05d}"][0]
            w += (adv / units_reg) * 8.0
        return w

    def get_saldo_width(s):
        w = 0.0
        for ch in s:
            cid = ord(ch)
            gid = (map_bold[cid*2] << 8) | map_bold[cid*2 + 1]
            adv = hmtx_bold[f"glyph{gid:05d}"][0]
            w += (adv / units_bold) * 8.0
        return w

    def get_reg_width(s):
        w = 0.0
        for ch in s:
            cid = ord(ch)
            gid = (map_reg[cid*2] << 8) | map_reg[cid*2 + 1]
            adv = hmtx_reg[f"glyph{gid:05d}"][0]
            w += (adv / units_reg) * 8.0
        return w

    def get_bold_width(s):
        w = 0.0
        for ch in s:
            cid = ord(ch)
            gid = (map_bold[cid*2] << 8) | map_bold[cid*2 + 1]
            adv = hmtx_bold[f"glyph{gid:05d}"][0]
            w += (adv / units_bold) * 8.0
        return w

    # Helper to update decompressed stream
    def update_stream(oid, transform_fn):
        raw = obj_raw[oid]
        m_stream = re.search(rb'stream[\r\n]+(.*?)[\r\n]+endstream', raw, re.DOTALL)
        stream_data = m_stream.group(1)
        decomp = zlib.decompress(stream_data)
        
        new_decomp = transform_fn(decomp)
        new_comp = zlib.compress(new_decomp, 9)
        
        before_stream = raw[:m_stream.start()]
        new_before_stream = re.sub(rb'/Length\s+\d+', f'/Length {len(new_comp)}'.encode(), before_stream)
        after_stream = raw[m_stream.end():]
        
        obj_raw[oid] = new_before_stream + b"stream\n" + new_comp + b"\nendstream" + after_stream

    # Identify Page Content streams: they contain the saldo color definition in PDF_OUT
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

    print(f"Discovered page content stream OIDs: {page_content_list}")
    assert len(page_content_list) == 5, f"Expected 5 page content streams, found {len(page_content_list)}"
    page_content_oids = {p_idx + 1: oid for p_idx, oid in enumerate(page_content_list)}

    # Row replacement regex:
    row_pattern = re.compile(
        rb'(q\s+1\s+0\s+0\s+1\s+(?:19\.\d+|20(?:\.0+)?)\s+([\d\.]+)\s+cm\s+BT\s+0\s+0\s+0\s+rg/R1\s+8\s+Tf(/R\d+\s+gs)(.*?)(0\.07451\s+0\.294118\s+0\.729412\s+rg/R2\s+8\s+Tf\s*\[\s*-?\d+\s*\(([^\)]*?)\)\s*\]TJ)\s+ET\s+Q)',
        re.DOTALL
    )

    PAGE_RIGHT_X = 563.80

    for p_num in range(1, 6):
        oid = page_content_oids[p_num]
        p_txs = [t for t in excel_tx_data if t["page"] == p_num]
        
        def make_page_patcher(pn, tx_list):
            def _patch(decomp):
                # 1. Patch No & Saldo for each row
                matches = list(row_pattern.finditer(decomp))
                assert len(matches) == len(tx_list), f"Page {pn}: expected {len(tx_list)} rows, matched {len(matches)}"
                
                # Replace in reverse order to preserve string offsets
                for i in reversed(range(len(matches))):
                    m = matches[i]
                    tx = tx_list[i]
                    y_str = m.group(2)
                    gs_str = m.group(3)
                    
                    no_str = str(tx["no"])
                    sal_str = tx["saldo_str"]
                    
                    w_no = get_no_width(no_str)
                    w_sal = get_saldo_width(sal_str)
                    calc_k = - round((551.00 - w_sal - w_no) / 0.008)
                    
                    no_u16 = to_utf16_be(no_str)
                    sal_u16 = to_utf16_be(sal_str)
                    
                    x_str = b"19.972" if pn == 1 else b"20"
                    repl = (
                        b"q 1 0 0 1 " + x_str + b" " + y_str + b" cm BT 0 0 0 rg/R1 8 Tf" + gs_str +
                        b"(" + no_u16 + b") Tj 0.07451 0.294118 0.729412 rg/R2 8 Tf[ " +
                        str(calc_k).encode() + b"(" + sal_u16 + b")]TJ ET Q"
                    )
                    decomp = decomp[:m.start()] + repl + decomp[m.end():]

                # 2. Patch Page Numbers (Bold 'P dari 5' and Italic 'P of 5')
                s_bold = f"{pn} dari 5"
                w_b = get_bold_width(s_bold)
                x_b = PAGE_RIGHT_X - w_b
                
                s_it = f"{pn} of 5"
                w_it = get_reg_width(s_it)
                x_it = PAGE_RIGHT_X - w_it

                # Collect all page number blocks to replace cleanly in reverse order
                page_num_replacements = []

                # Italic block: q 1 0 0 1 <x> 726 cm BT 0 0 0 rg/R3 8 Tf/<gs> gs... ET Q
                m_it = re.search(rb'q\s+1\s+0\s+0\s+1\s+[\d\.]+\s+726\s+cm\s+BT\s+0\s+0\s+0\s+rg/R3\s+8\s+Tf(/R\d+\s+gs).*?ET\s+Q', decomp, re.DOTALL)
                assert m_it is not None, f"Page {pn}: italic page number block not found"
                gs_it = m_it.group(1)
                new_it = (
                    f"q 1 0 0 1 {x_it:.2f} 726 cm BT 0 0 0 rg/R1 8 Tf 1 0 0.2 1 0 0 Tm".encode() +
                    gs_it + b"(" + to_utf16_be(s_it) + b") Tj ET Q"
                )
                page_num_replacements.append((m_it.start(), m_it.end(), new_it))

                # Bold blocks at y=736:
                bold_blocks = list(re.finditer(rb'q\s+1\s+0\s+0\s+1\s+[\d\.]+\s+736\s+cm\s+BT\s+0\s+0\s+0\s+rg/R2\s+8\s+Tf(/R\d+\s+gs).*?ET\s+Q', decomp, re.DOTALL))
                if bold_blocks:
                    gs_b = bold_blocks[-1].group(1)
                    new_b = (
                        f"q 1 0 0 1 {x_b:.2f} 736 cm BT 0 0 0 rg/R2 8 Tf".encode() +
                        gs_b + b"(" + to_utf16_be(s_bold) + b") Tj ET Q"
                    )
                    # Replace first bold block with new_b, erase any subsequent
                    page_num_replacements.append((bold_blocks[0].start(), bold_blocks[0].end(), new_b))
                    for extra_bb in bold_blocks[1:]:
                        page_num_replacements.append((extra_bb.start(), extra_bb.end(), b""))

                # Apply page number replacements in reverse order of start position
                page_num_replacements.sort(key=lambda x: x[0], reverse=True)
                for start_pos, end_pos, repl_bytes in page_num_replacements:
                    decomp = decomp[:start_pos] + repl_bytes + decomp[end_pos:]

                print(f"Patched Page {pn} (Obj {oid}): {len(tx_list)} rows + Page Numbers ({s_bold} / {s_it})")
                return decomp
            return _patch

        update_stream(oid, make_page_patcher(p_num, p_txs))

    # Reassemble PDF and regenerate XRef Stream
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
        str(xref_oid).encode() + b' 0 obj\n<<' + new_xref_dict + b'>>\nstream\n' +
        comp_xref + b'\nendstream\nendobj\nstartxref\n' + str(xref_start).encode() + b'\n%%EOF\n'
    )
    out.extend(xref_obj_str)

    with open(PDF_OUT, "wb") as f:
        f.write(out)

    print(f"\nSaved perfected PDF: {PDF_OUT} ({len(out)} bytes)")
    print("=================================================================")
    print("BUILD COMPLETED SUCCESSFULLY!")
    print("=================================================================")

if __name__ == "__main__":
    run_build()
