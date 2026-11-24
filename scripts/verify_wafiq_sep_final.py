"""
Comprehensive Verification and Audit for Bank Mandiri e-Statement:
Client: WAFIQ DWI ANANDA
Period: September 2026 (01 Sep 2026 - 30 Sep 2026)
"""

import pdfplumber
import openpyxl
import re

pdf_path = "output/REK_WAFIQ_SEP_OUTPUT_1.pdf"
excel_path = "output/Template_Mutasi_SEP_OUTPUT_1.xlsx"

print("=================================================================")
print("COMPREHENSIVE AUDIT REPORT: WAFIQ DWI ANANDA - SEPTEMBER 2026")
print("=================================================================")

with pdfplumber.open(pdf_path) as pdf:
    print(f"Total Pages: {len(pdf.pages)}")
    assert len(pdf.pages) == 5, f"Expected 5 pages, found {len(pdf.pages)}"

    # 1. SUMMARY BOX AUDIT (Page 1)
    print("\n--- 1. SUMMARY BOX GEOMETRY & ALIGNMENT AUDIT (PAGE 1) ---")
    p1 = pdf.pages[0]
    words = p1.extract_words()
    sb_words = [w for w in words if 280 <= w['x0'] <= 580 and 150 <= w['top'] <= 260]
    sb_words.sort(key=lambda w: (round(w['top'], 1), w['x0']))

    rows = {}
    for w in sb_words:
        top_k = round(w['top'], 1)
        rows.setdefault(top_k, []).append(w)

    for top_k, wlist in sorted(rows.items()):
        line_text = " ".join([w['text'] for w in wlist])
        min_x = min(w['x0'] for w in wlist)
        max_x = max(w['x1'] for w in wlist)
        print(f"Top {top_k:5.2f} pt | X: [{min_x:6.2f} .. {max_x:6.2f}] | Content: {line_text}")

    # Check colon alignment
    colons = [w for w in sb_words if w['text'] == ':']
    print(f"\nColons count: {len(colons)}")
    for c in colons:
        print(f"Colon at top={c['top']:.2f}, x0={c['x0']:.2f}, x1={c['x1']:.2f}")

    # Check values right edge
    print("\nSummary Values right alignment:")
    for w in sb_words:
        if ',' in w['text'] and w['x0'] > 500:
            print(f"Value '{w['text']:<20}' x0={w['x0']:<6.2f} x1={w['x1']:<6.2f} top={w['top']:<6.2f}")

    # 2. PAGE NUMBERS AUDIT (Pages 1..4)
    print("\n--- 2. PAGE NUMBERS AUDIT ACROSS PAGES 1..4 ---")
    for p_idx in range(4):
        p_num = p_idx + 1
        page = pdf.pages[p_idx]
        words = page.extract_words()
        pn_words = [w for w in words if 90 <= w['top'] <= 125 and w['x0'] > 500]
        pn_text = " ".join([w['text'] for w in sorted(pn_words, key=lambda x: (x['top'], x['x0']))])
        print(f"Page {p_num}: {pn_text}")

    # 3. HEADER METADATA AUDIT (Pages 1..4)
    print("\n--- 3. HEADER METADATA AUDIT (PAGES 1..4) ---")
    for p_idx in range(4):
        p_num = p_idx + 1
        page = pdf.pages[p_idx]
        h_words = [w for w in page.extract_words() if w['top'] < 160]
        h_text = " ".join([w['text'] for w in sorted(h_words, key=lambda x: (x['top'], x['x0']))])
        for label, pattern in [
            ("Nama/Name", "WAFIQ DWI ANANDA"),
            ("Cabang/Branch", "KCP Serang Ciceri"),
            ("Periode/Period", "01 Sep 2026 - 30 Sep 2026"),
            ("Dicetak pada/Issued on", "12 Nov 2026"),
        ]:
            found = pattern in h_text
            print(f"Page {p_num} '{label}': {pattern} -> {'PASS' if found else 'FAIL'}")
    
    # Account Number on Page 1
    p1_words = [w for w in p1.extract_words() if w['top'] < 250]
    p1_text = " ".join([w['text'] for w in sorted(p1_words, key=lambda x: (x['top'], x['x0']))])
    print(f"Page 1 Account Number: 1630016689138 -> {'PASS' if '1630016689138' in p1_text else 'FAIL'}")

    # 4. TABLE TRANSACTIONS & SALDO AUDIT
    print("\n--- 4. TABLE TRANSACTIONS & SALDO AUDIT ---")
    total_tx = 0
    for p_idx in range(4):
        p_num = p_idx + 1
        page = pdf.pages[p_idx]
        words = page.extract_words()
        min_top = 310 if p_num == 1 else 180
        t_words = [w for w in words if min_top <= w['top'] <= 780]
        wibs = sorted([w for w in t_words if w['text'] == 'WIB'], key=lambda x: x['top'])
        total_tx += len(wibs)
        print(f"\nPage {p_num} ({len(wibs)} transactions):")
        for pick_idx, tag in [(0, "First"), (len(wibs)-1, "Last")]:
            w = wibs[pick_idx]
            y = w['top']
            row_words = [x for x in t_words if abs(x['top'] - y) < 15]
            row_words.sort(key=lambda x: x['x0'])
            row_line = " | ".join([f"{x['text']} (x0={x['x0']:.1f}, x1={x['x1']:.1f})" for x in row_words])
            print(f"  {tag} Tx: {row_line}")

    print(f"\nTotal transactions audited: {total_tx}")

    # 5. SPECIAL TRANSACTIONS AUDIT
    print("\n--- 5. SPECIAL TRANSACTIONS AUDIT ---")
    # Tx 33 (Salary on Page 3)
    p3 = pdf.pages[2]
    p3_words = p3.extract_words()
    sal_words = [w for w in p3_words if 665 <= w['top'] <= 705]
    print("Tx 33 (Salary) Words on Page 3:")
    for w in sorted(sal_words, key=lambda x: (x['top'], x['x0'])):
        print(f"  Top {w['top']:.2f}, x0={w['x0']:.2f}-{w['x1']:.2f}: {w['text']}")

    # Tx 46 (Closing Fee on Page 4)
    p4 = pdf.pages[3]
    p4_words = p4.extract_words()
    close_words = [w for w in p4_words if 725 <= w['top'] <= 745]
    print("\nTx 46 (Closing Fee) Words on Page 4:")
    for w in sorted(close_words, key=lambda x: (x['top'], x['x0'])):
        print(f"  Top {w['top']:.2f}, x0={w['x0']:.2f}-{w['x1']:.2f}: {w['text']}")

    # Check font purity
    all_fonts = set()
    for page in pdf.pages:
        for char in page.chars:
            all_fonts.add(char.get('fontname', ''))
    print(f"\nAll Fonts in PDF: {all_fonts}")
    foreign_fonts = [f for f in all_fonts if "TTInterphases" not in f and f != '']
    print(f"Foreign fonts (should be none): {foreign_fonts}")

# 6. EXCEL RECONCILIATION SHEET AUDIT
print("\n--- 6. EXCEL RECONCILIATION SHEET AUDIT ---")
wb = openpyxl.load_workbook(excel_path)
ws_hr = wb['Header & Ringkasan']
print("B10 (Nama):", ws_hr['B10'].value)
print("B11 (Cabang):", ws_hr['B11'].value)
print("B12 (Periode):", ws_hr['B12'].value)
print("B13 (Dicetak):", ws_hr['B13'].value)
print("B14 (No Rek):", ws_hr['B14'].value)
print("B22 (Saldo Awal):", ws_hr['B22'].value)
print("B23 (Dana Masuk):", ws_hr['B23'].value)
print("B24 (Dana Keluar):", ws_hr['B24'].value)
print("B25 (Saldo Akhir):", ws_hr['B25'].value)
print("B26 (Status):", ws_hr['B26'].value)

ws_tm = wb['Tabel_Mutasi']
empty_no = sum(1 for r in range(6, 54) if ws_tm.cell(r, 1).value is None and ws_tm.cell(r, 5).value not in [0, None])
empty_dt = sum(1 for r in range(6, 54) if ws_tm.cell(r, 2).value is None and ws_tm.cell(r, 5).value not in [0, None])
empty_tm = sum(1 for r in range(6, 54) if ws_tm.cell(r, 3).value is None and ws_tm.cell(r, 5).value not in [0, None])
empty_dc = sum(1 for r in range(6, 54) if ws_tm.cell(r, 4).value is None and ws_tm.cell(r, 5).value not in [0, None])
print(f"\nEmpty No in Excel: {empty_no}")
print(f"Empty Tanggal in Excel: {empty_dt}")
print(f"Empty Jam in Excel: {empty_tm}")
print(f"Empty Desc in Excel: {empty_dc}")
print(f"Tx 33 (Salary) in Excel: No={ws_tm.cell(40, 1).value}, Date={ws_tm.cell(40, 2).value}, Time={ws_tm.cell(40, 3).value}, Nom={ws_tm.cell(40, 5).value}")
print(f"Tx 33 Desc in Excel: {repr(ws_tm.cell(40, 4).value)}")
print(f"Tx 46 (Closing Fee) in Excel: No={ws_tm.cell(53, 1).value}, Date={ws_tm.cell(53, 2).value}, Time={ws_tm.cell(53, 3).value}, Nom={ws_tm.cell(53, 5).value}")
print(f"Tx 46 Desc in Excel: {repr(ws_tm.cell(53, 4).value)}")
