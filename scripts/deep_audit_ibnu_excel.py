import openpyxl

excel_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\Template_Mutasi_AUG.xlsx"
wb = openpyxl.load_workbook(excel_path, data_only=True)
ws = wb['Tabel_Mutasi']

print(f"Max row: {ws.max_row}")

populated_rows = []
for r in range(5, ws.max_row + 1):
    vals = [ws.cell(r, c).value for c in range(1, 8)]
    if any(v is not None for v in vals):
        populated_rows.append((r, vals))

print(f"Total populated rows (including row 5 initial): {len(populated_rows)}")
print(f"Total transaction rows: {len(populated_rows) - 1}")

print("\n--- FIRST 10 TRANSACTIONS ---")
for r, vals in populated_rows[:11]:
    print(f"Row {r:3d}: {vals}")

print("\n--- CHECKING ROWS WITH KETERANGAN OR DATE OR SALARY ---")
for r, vals in populated_rows:
    nom = vals[4]
    ket = vals[3]
    tgl = vals[1]
    # Check if keterangan is filled, or if nominal is salary-like (> 1,000,000 positive)
    if ket is not None or tgl is not None or (nom is not None and nom > 1000000):
        print(f"Row {r:3d}: No={vals[0]} Tgl={tgl} Jam={vals[2]} Ket={ket} Nom={nom} Saldo={vals[6]}")

print("\n--- LAST 10 TRANSACTIONS ---")
for r, vals in populated_rows[-10:]:
    print(f"Row {r:3d}: {vals}")
