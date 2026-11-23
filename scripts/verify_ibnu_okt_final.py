import pdfplumber
import openpyxl
import re

pdf_path = "output/REK_IBNU_OKT_OUTPUT_1.pdf"
xlsx_path = "output/Template_Mutasi_OKT_OUTPUT_1.xlsx"

print("=================================================================")
print("COMPREHENSIVE AUDIT REPORT: IBNU AGUN - OKTOBER 2026")
print("=================================================================")

# 1. SUMMARY BOX GEOMETRY & ALIGNMENT
print("\n--- 1. SUMMARY BOX GEOMETRY & ALIGNMENT AUDIT (PAGE 1) ---")
with pdfplumber.open(pdf_path) as pdf:
    p1 = pdf.pages[0]
    words = p1.extract_words()
    
    # Check baseline lines in Summary Box (top: 165..245, x: 290..575)
    sb_words = [w for w in words if 290 <= w['x0'] <= 575 and 165 <= w['top'] <= 245]
    lines_by_top = {}
    for w in sb_words:
        t_key = round(w['top'], 1)
        # bucket within 2 pt
        found_bucket = None
        for b in lines_by_top:
            if abs(b - t_key) < 2.0:
                found_bucket = b
                break
        if found_bucket is not None:
            lines_by_top[found_bucket].append(w)
        else:
            lines_by_top[t_key] = [w]
            
    for t_key in sorted(lines_by_top.keys()):
        lw = sorted(lines_by_top[t_key], key=lambda x: x['x0'])
        text_line = " ".join(x['text'] for x in lw)
        x_min = min(x['x0'] for x in lw)
        x_max = max(x['x1'] for x in lw)
        print(f"Top {t_key:6.2f} pt | X: [{x_min:6.2f} .. {x_max:6.2f}] | Content: {text_line}")

    # Check colons
    colons = [w for w in sb_words if w['text'] == ':']
    print(f"\nColons count: {len(colons)}")
    for c in colons:
        print(f"Colon at top={c['top']:.2f}, x0={c['x0']:.2f}, x1={c['x1']:.2f}")

    # Check right alignment of summary values
    print("\nSummary Values right alignment:")
    for w in sb_words:
        if any(w['text'].startswith(prefix) for prefix in ['8.742', '+', '-', '5.599']):
            print(f"Value '{w['text']:20s}' x0={w['x0']:.2f} x1={w['x1']:.2f} top={w['top']:.2f}")

    # Check slashes in labels
    print("\nSlash in labels check:")
    for w in sb_words:
        if '/' in w['text']:
            print(f"Label with slash: '{w['text']}' top={w['top']:.2f} x0={w['x0']:.2f} x1={w['x1']:.2f}")

# 2. PAGE NUMBERS
print("\n--- 2. PAGE NUMBERS AUDIT ACROSS ALL 7 PAGES ---")
with pdfplumber.open(pdf_path) as pdf:
    print(f"Total Pages in PDF: {len(pdf.pages)}")
    for p_idx in range(len(pdf.pages)):
        p = pdf.pages[p_idx]
        words = p.extract_words()
        pn_words = [w for w in words if w['top'] < 130 and w['x0'] > 500]
        pn_text = " ".join(w['text'] for w in sorted(pn_words, key=lambda x: (x['top'], x['x0'])))
        if p_idx == 6:
            # Check disclaimer text on page 7
            t7 = p.extract_text()
            discl = "DISCLAIMER PAGE VERIFIED" if "ini adalah batas akhir transaksi anda" in t7 else "UNKNOWN"
            print(f"Page 7: {discl}")
        else:
            print(f"Page {p_idx+1}: {pn_text}")

# 3. HEADER METADATA
print("\n--- 3. HEADER METADATA AUDIT (PAGE 1) ---")
with pdfplumber.open(pdf_path) as pdf:
    p1 = pdf.pages[0]
    p1_text = p1.extract_text()
    for field, expected in [
        ("Nama/Name", "IBNU AGUN"),
        ("Cabang/Branch", "KCP Serang Ciceri"),
        ("Periode/Period", "01 Oct 2026 - 31 Oct 2026"),
        ("Dicetak pada/Issued on", "12 Nov 2026"),
        ("Nomor Rekening", "1630016072145")
    ]:
        status = "PASS" if expected in p1_text else "FAIL"
        print(f"Header '{field}': {expected} -> {status}")

# 4. TABLE TRANSACTIONS & SALDO AUDIT
print("\n--- 4. TABLE TRANSACTIONS & SALDO AUDIT ---")
with pdfplumber.open(pdf_path) as pdf:
    for p_idx in range(6):
        p = pdf.pages[p_idx]
        words = p.extract_words()
        min_top = 310 if p_idx == 0 else 180
        col_no = [w for w in words if 15 <= w['x0'] <= 35 and min_top <= w['top'] <= 780 and w['text'].isdigit()]
        col_no.sort(key=lambda w: w['top'])
        print(f"\nPage {p_idx+1} ({len(col_no)} transactions):")
        
        # Check first and last tx on this page
        for w_target in [col_no[0], col_no[-1]]:
            y = w_target['top']
            row_words = [w for w in words if abs(w['top'] - y) <= 12]
            row_words.sort(key=lambda x: x['x0'])
            row_summary = " | ".join(f"{w['text']} (x0={w['x0']:.1f}, x1={w['x1']:.1f})" for w in row_words)
            tx_label = "First Tx" if w_target == col_no[0] else "Last Tx"
            print(f"  {tx_label}: {row_summary}")

# 5. EXCEL RECONCILIATION SHEET AUDIT
print("\n--- 5. EXCEL RECONCILIATION SHEET AUDIT ---")
wb = openpyxl.load_workbook(xlsx_path, data_only=True)
ws_hr = wb["Header & Ringkasan"]
for cell_ref, label in [
    ('B10', 'Nama'),
    ('B11', 'Cabang'),
    ('B12', 'Periode'),
    ('B13', 'Dicetak'),
    ('B14', 'No Rek'),
    ('B22', 'Saldo Awal'),
    ('B23', 'Dana Masuk'),
    ('B24', 'Dana Keluar'),
    ('B25', 'Saldo Akhir'),
    ('B26', 'Status')
]:
    print(f"{cell_ref} ({label}): {ws_hr[cell_ref].value}")
