import pdfplumber
import openpyxl

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_SEP_2026_PERFECT.pdf"
excel_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\Template_Mutasi_SEP_Reconciled.xlsx"

print("==================================================")
print("FINAL COMPREHENSIVE AUDIT REPORT: SEPTEMBER 2026")
print("==================================================")

with pdfplumber.open(pdf_path) as pdf:
    print(f"\n1. PDF Page Count: {len(pdf.pages)}")
    
    total_foreign = 0
    for p_idx, page in enumerate(pdf.pages, 1):
        foreign = [c for c in page.chars if 'TTInterphases' not in c.get('fontname', '')]
        total_foreign += len(foreign)
        fonts = set(c.get('fontname') for c in page.chars)
        print(f"   Page {p_idx}: {len(page.extract_words())} words | Fonts: {fonts}")
    print(f"   Total Foreign Font Characters: {total_foreign} (100% Authentic Mandiri Font: {'PASS' if total_foreign == 0 else 'FAIL'})")
    
    # Page 1 Account Number Check
    p1_words = pdf.pages[0].extract_words()
    acc_word = [w for w in p1_words if "163001" in w['text']]
    if acc_word:
        w = acc_word[0]
        print(f"\n2. Nomor Rekening Position:")
        print(f"   Text: '{w['text']}' at x0={w['x0']:.2f} pt (Target: 160.00 pt) -> {'PASS' if abs(w['x0']-160.0) < 0.1 else 'FAIL'}")

    # Check 35 Transactions
    print("\n3. Transaction Chronology & Alignment Check:")
    all_dt = []
    for page_idx, page in enumerate(pdf.pages, 1):
        words = page.extract_words()
        no_words = [w for w in words if abs(w['x0'] - 20.0) < 5 and 200 < w['top'] < 780 and w['text'].isdigit()]
        no_words.sort(key=lambda w: w['top'])
        for nw in no_words:
            no_val = int(nw['text'])
            y = nw['top']
            d_words = [w for w in words if 45 <= w['x0'] < 118 and abs(w['top'] - (y - 4)) < 8]
            t_words = [w for w in words if 45 <= w['x0'] < 118 and abs(w['top'] - (y + 5)) < 8]
            d_str = " ".join(w['text'] for w in sorted(d_words, key=lambda x: x['x0']))
            t_str = " ".join(w['text'] for w in sorted(t_words, key=lambda x: x['x0']))
            all_dt.append((no_val, page_idx, d_str, t_str))
            
    print(f"   Found {len(all_dt)} transaction rows in PDF.")
    print(f"   First tx: Row {all_dt[0][0]} -> {all_dt[0][2]} {all_dt[0][3]}")
    print(f"   Gaji tx : Row {all_dt[21][0]} -> {all_dt[21][2]} {all_dt[21][3]}")
    print(f"   Post-gaji tx 23: Row {all_dt[22][0]} -> {all_dt[22][2]} {all_dt[22][3]}")
    print(f"   Last tx : Row {all_dt[-1][0]} -> {all_dt[-1][2]} {all_dt[-1][3]}")

# Check Excel
wb = openpyxl.load_workbook(excel_path, data_only=True)
ws1 = wb["Header & Ringkasan"]
ws2 = wb["Tabel_Mutasi"]
print("\n4. Excel Audit Verification:")
print(f"   Nasabah       : {ws1['B10'].value}")
print(f"   Cabang        : {ws1['B11'].value}")
print(f"   Periode       : {ws1['B12'].value}")
print(f"   Saldo Awal    : {ws1['B22'].value:,.2f}")
print(f"   Dana Masuk    : {ws1['B23'].value:,.2f}")
print(f"   Dana Keluar   : {ws1['B24'].value:,.2f}")
print(f"   Saldo Akhir   : {ws1['B25'].value:,.2f}")
print(f"   Tabel_Mutasi rows count: {ws2.max_row}")
