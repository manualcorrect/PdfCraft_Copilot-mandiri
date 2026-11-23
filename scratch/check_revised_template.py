import openpyxl
import pdfplumber
import os

excel_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\Template_Mutasi_Aug.xlsx"
pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\2.pdf"

print("========================================")
print("1. CHECK EXCEL HEADER & RINGKASAN")
print("========================================")
wb = openpyxl.load_workbook(excel_path, data_only=True)
ws1 = wb["Header & Ringkasan"]
for r in range(1, ws1.max_row + 1):
    k = ws1.cell(r, 1).value
    v = ws1.cell(r, 2).value
    if k or v:
        print(f"Row {r:2d}: {k} -> {v}")

print("\n========================================")
print("2. CHECK EXCEL TABEL_MUTASI")
print("========================================")
ws2 = wb["Tabel_Mutasi"]
tx_rows = []
for r in range(5, ws2.max_row + 1):
    vals = [ws2.cell(r, c).value for c in range(1, 8)]
    if any(x is not None for x in vals):
        tx_rows.append((r, vals))

print(f"Total transaction rows found: {len(tx_rows)}")
for r, vals in tx_rows:
    print(f"Row {r:2d}: {vals}")

print("\n========================================")
print("3. CHECK PDF 2.pdf LAYOUT & ROWS")
print("========================================")
with pdfplumber.open(pdf_path) as pdf:
    print(f"Total pages: {len(pdf.pages)}")
    for i, p in enumerate(pdf.pages):
        words = p.extract_words()
        min_top = 320 if i == 0 else 200
        # Row numbers
        nos = [w for w in words if min_top <= w["top"] <= 800 and 15 <= w["x0"] <= 35 and w["text"].isdigit()]
        print(f"Page {i+1} (top {min_top}-800): {len(nos)} tx rows -> {[w['text'] for w in nos]}")
        if i == 3:
            # Check disclaimer position
            disc_words = [w for w in words if "Disclaimer" in w["text"] or "batas akhir" in w["text"]]
            for dw in disc_words:
                print(f"  Disclaimer element: '{dw['text']}' at top={dw['top']:.2f}, bottom={dw['bottom']:.2f}")

print("\n========================================")
print("4. FINANCIAL SUMMARY AUDIT")
print("========================================")
sawal = ws1.cell(22, 2).value
dmasuk = ws1.cell(23, 2).value
dkeluar = ws1.cell(24, 2).value
sakhir = ws1.cell(25, 2).value

print(f"Saldo Awal   : {sawal}")
print(f"Dana Masuk   : {dmasuk}")
print(f"Dana Keluar  : {dkeluar}")
print(f"Saldo Akhir  : {sakhir}")
calc_akhir = (sawal or 0) + (dmasuk or 0) - (dkeluar or 0)
print(f"Kalkulasi Saldo Akhir (Awal + Masuk - Keluar): {calc_akhir}")
if sakhir is not None:
    diff = calc_akhir - sakhir
    print(f"Selisih dengan Saldo Akhir di Excel: {diff}")
