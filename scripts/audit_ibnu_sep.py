import os
import openpyxl
import pdfplumber
import re

base_dir = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\sep"
pdf_path = os.path.join(base_dir, "0.pdf")
excel_path = os.path.join(base_dir, "Template_Mutasi_SEP.xlsx")

print("=================================================================")
print("DEEP AUDIT: IBNU AGUN - SEPTEMBER 2026")
print("=================================================================")

# 1. PDF INSPECTION
print("\n--- 1. 0.PDF STRUCTURE ---")
with pdfplumber.open(pdf_path) as pdf:
    print(f"Total Pages in 0.pdf: {len(pdf.pages)}")
    total_wibs = 0
    for p_idx, page in enumerate(pdf.pages):
        words = page.extract_words()
        min_top = 310 if p_idx == 0 else 180
        t_words = [w for w in words if min_top <= w['top'] <= 780]
        wibs = sorted([w for w in t_words if w['text'] == 'WIB'], key=lambda x: x['top'])
        print(f"Page {p_idx+1}: {len(wibs)} transactions")
        total_wibs += len(wibs)
        if p_idx == 0:
            # Check Header & Summary Box
            sb_words = [w for w in words if 280 <= w['x0'] <= 580 and 150 <= w['top'] <= 260]
            print("  Page 1 Summary Box words count:", len(sb_words))
            hdr_words = [w for w in words if w['top'] < 140]
            print("  Page 1 Header text:", " ".join(w['text'] for w in sorted(hdr_words, key=lambda x: (x['top'], x['x0']))))
            acc_words = [w for w in words if 180 <= w['top'] <= 210 and w['x0'] < 300]
            print("  Page 1 Account area:", " ".join(w['text'] for w in sorted(acc_words, key=lambda x: (x['top'], x['x0']))))
            
    print(f"Total Transactions in 0.pdf: {total_wibs}")

# 2. EXCEL INSPECTION
print("\n--- 2. EXCEL INSPECTION ---")
wb = openpyxl.load_workbook(excel_path, data_only=True)
print("Sheets:", wb.sheetnames)

ws_hr = wb['Header & Ringkasan']
print("\nHeader & Ringkasan Sheet:")
for r in range(1, 30):
    val_a = ws_hr.cell(r, 1).value
    val_b = ws_hr.cell(r, 2).value
    if val_a or val_b:
        print(f"  Row {r:2d}: {val_a:<45} | {val_b}")

ws_tm = wb['Tabel_Mutasi']
print(f"\nTabel_Mutasi max_row: {ws_tm.max_row}")
print(f"Row 5 (Awal): {[ws_tm.cell(5, c).value for c in range(1, 8)]}")

active_rows = []
dummy_rows = []
for r in range(6, ws_tm.max_row + 1):
    nom = ws_tm.cell(r, 5).value
    saldo = ws_tm.cell(r, 7).value
    ket = ws_tm.cell(r, 4).value
    no = ws_tm.cell(r, 1).value
    if nom is None or abs(float(nom)) < 0.001:
        dummy_rows.append((r, no, nom, ket))
    else:
        active_rows.append((r, no, float(nom), float(saldo), ket))

print(f"Active rows count: {len(active_rows)}")
print(f"Dummy rows (nominal 0/None): {len(dummy_rows)} -> {dummy_rows}")

pos_sum = sum(x[2] for x in active_rows if x[2] > 0)
neg_sum = sum(x[2] for x in active_rows if x[2] < 0)
awal_val = float(ws_tm.cell(5, 7).value) if ws_tm.cell(5, 7).value is not None else 0.0
last_saldo = active_rows[-1][3] if active_rows else 0.0

print(f"\nFinancial Calculations:")
print(f"  Saldo Awal (Row 5): {awal_val:,.2f}")
print(f"  Total Kredit (Dana Masuk): +{pos_sum:,.2f}")
print(f"  Total Debit (Dana Keluar): {neg_sum:,.2f}")
print(f"  Calculated Saldo Akhir: {awal_val + pos_sum + neg_sum:,.2f}")
print(f"  Last Row Saldo Berjalan: {last_saldo:,.2f}")
print(f"  Difference: {awal_val + pos_sum + neg_sum - last_saldo:,.2f}")

# Check for salary row (+6.000.000 or similar)
sal_rows = [x for x in active_rows if x[2] >= 5000000]
print(f"\nPotential Salary Rows (>= 5,000,000): {sal_rows}")

# Check last row (closing fee)
print(f"Last Row (Row {active_rows[-1][0]}): Nom={active_rows[-1][2]} | Ket={active_rows[-1][4]}")
