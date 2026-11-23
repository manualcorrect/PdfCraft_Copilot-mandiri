import pdfplumber
import openpyxl

pdf_path = "output/REK_IBNU_AUG_OUTPUT_1.pdf"
excel_path = "output/Template_Mutasi_AUG_OUTPUT_1.xlsx"

print("=================================================================")
print("COMPREHENSIVE AUDIT REPORT: IBNU AGUN - AUGUST 2026")
print("=================================================================")

with pdfplumber.open(pdf_path) as pdf:
    print(f"Total Pages: {len(pdf.pages)}")
    
    # 1. SUMMARY BOX AUDIT (Page 1)
    print("\n--- 1. SUMMARY BOX GEOMETRY & ALIGNMENT AUDIT (PAGE 1) ---")
    p1 = pdf.pages[0]
    words = p1.extract_words()
    sb_words = [w for w in words if 280 <= w['x0'] <= 580 and 150 <= w['top'] <= 260]
    sb_words.sort(key=lambda w: (round(w['top'], 1), w['x0']))
    
    rows = {}
    for w in sb_words:
        top_k = round(w['top'], 1)
        if top_k not in rows:
            rows[top_k] = []
        rows[top_k].append(w)
        
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

    # Check slash character in labels
    print("\nSlash in labels check:")
    for w in sb_words:
        if '/' in w['text']:
            print(f"Label with slash: '{w['text']}' top={w['top']:.2f} x0={w['x0']:.2f} x1={w['x1']:.2f}")

    # 2. PAGE NUMBERS AUDIT (Pages 1..7)
    print("\n--- 2. PAGE NUMBERS AUDIT ACROSS ALL 7 PAGES ---")
    for p_idx, page in enumerate(pdf.pages):
        p_num = p_idx + 1
        words = page.extract_words()
        pn_words = [w for w in words if 90 <= w['top'] <= 125 and w['x0'] > 500]
        pn_text = " ".join([w['text'] for w in sorted(pn_words, key=lambda x: (x['top'], x['x0']))])
        print(f"Page {p_num}: {pn_text}")

    # 3. HEADER METADATA AUDIT (Page 1)
    print("\n--- 3. HEADER METADATA AUDIT (PAGE 1) ---")
    h_words = [w for w in words if w['top'] < 300]
    for label, pattern in [
        ("Nama/Name", "IBNU AGUN"),
        ("Cabang/Branch", "KCP Serang Ciceri"),
        ("Periode/Period", "01 Aug 2026 - 31 Aug 2026"),
        ("Dicetak pada/Issued on", "12 Nov 2026"),
        ("Nomor Rekening", "1630016072145")
    ]:
        found = any(pattern in w['text'] or pattern in " ".join([x['text'] for x in h_words]) for w in h_words)
        print(f"Header '{label}': {pattern} -> {'PASS' if found else 'FAIL'}")

    # 4. TABLE TRANSACTIONS & SALDO AUDIT
    print("\n--- 4. TABLE TRANSACTIONS & SALDO AUDIT ---")
    for p_idx, page in enumerate(pdf.pages):
        p_num = p_idx + 1
        words = page.extract_words()
        min_top = 310 if p_num == 1 else 180
        t_words = [w for w in words if min_top <= w['top'] <= 780]
        wibs = sorted([w for w in t_words if w['text'] == 'WIB'], key=lambda x: x['top'])
        
        # Check first and last tx on this page
        print(f"\nPage {p_num} ({len(wibs)} transactions):")
        for pick_idx, tag in [(0, "First"), (len(wibs)-1, "Last")]:
            w = wibs[pick_idx]
            y = w['top']
            # Find no, date, time, nom, saldo
            row_words = [x for x in t_words if abs(x['top'] - y) < 15]
            row_words.sort(key=lambda x: x['x0'])
            row_line = " | ".join([f"{x['text']} (x0={x['x0']:.1f}, x1={x['x1']:.1f})" for x in row_words])
            print(f"  {tag} Tx: {row_line}")

# 5. EXCEL AUDIT
print("\n--- 5. EXCEL RECONCILIATION SHEET AUDIT ---")
wb = openpyxl.load_workbook(excel_path, data_only=True)
ws_hr = wb['Header & Ringkasan']
print(f"B10 (Nama): {ws_hr['B10'].value}")
print(f"B11 (Cabang): {ws_hr['B11'].value}")
print(f"B12 (Periode): {ws_hr['B12'].value}")
print(f"B13 (Dicetak): {ws_hr['B13'].value}")
print(f"B14 (No Rek): {ws_hr['B14'].value}")
print(f"B22 (Saldo Awal): {ws_hr['B22'].value}")
print(f"B23 (Dana Masuk): {ws_hr['B23'].value}")
print(f"B24 (Dana Keluar): {ws_hr['B24'].value}")
print(f"B25 (Saldo Akhir): {ws_hr['B25'].value}")
print(f"B26 (Status): {ws_hr['B26'].value}")
