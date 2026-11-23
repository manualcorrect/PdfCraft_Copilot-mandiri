import openpyxl

excel_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\Template_Mutasi_AUG.xlsx"
wb = openpyxl.load_workbook(excel_path, data_only=True)
ws = wb['Tabel_Mutasi']

saldo_awal = float(ws.cell(5, 7).value) + 0.81
print(f"Saldo Awal (with .81): {saldo_awal:,.2f}")

total_cr = 0
total_db = 0
running_saldo = saldo_awal

# Check with Row 16 & 17 included vs excluded
print("\n--- CALCULATING WITH EXCLUDED ZERO ROWS ---")
for r in range(6, ws.max_row + 1):
    nom = ws.cell(r, 5).value
    if nom is None:
        continue
    if nom == 0:
        print(f"Row {r} is zero, skipping")
        continue
    if nom > 0:
        total_cr += nom
    else:
        total_db += abs(nom)
    running_saldo += nom
    excel_saldo = ws.cell(r, 7).value + 0.81
    if abs(running_saldo - excel_saldo) > 0.01:
        print(f"Mismatch at Row {r}: calculated={running_saldo:,.2f} vs excel={excel_saldo:,.2f}")

print(f"\nTotal Dana Masuk (+): {total_cr:,.2f}")
print(f"Total Dana Keluar (-): {total_db:,.2f}")
print(f"Calculated Saldo Akhir: {running_saldo:,.2f}")

# Check Summary in Header & Ringkasan
ws_hr = wb['Header & Ringkasan']
print("\n--- HEADER & RINGKASAN SHEET ---")
for r in range(20, ws_hr.max_row + 1):
    vals = [ws_hr.cell(r, c).value for c in range(1, 6)]
    if any(v is not None for v in vals):
        print(f"Row {r:2d}: {vals}")
