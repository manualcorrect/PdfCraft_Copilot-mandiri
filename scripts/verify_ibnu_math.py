import openpyxl

wb = openpyxl.load_workbook(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\Template_Mutasi_AUG.xlsx", data_only=True)
ws = wb['Tabel_Mutasi']

pos_sum = 0
neg_sum = 0
active_rows = []

for r in range(6, ws.max_row + 1):
    nom = ws.cell(r, 5).value
    saldo = ws.cell(r, 7).value
    if nom is not None and abs(float(nom)) > 0.001:
        f_nom = float(nom)
        f_saldo = float(saldo)
        if f_nom > 0:
            pos_sum += f_nom
        else:
            neg_sum += f_nom
        active_rows.append((r, f_nom, f_saldo))

print("Active rows count:", len(active_rows))
print(f"Total Kredit (Dana Masuk): {pos_sum:,.2f}")
print(f"Total Debit (Dana Keluar): {neg_sum:,.2f}")
print(f"First row (row {active_rows[0][0]}): nom={active_rows[0][1]}, saldo={active_rows[0][2]}")
print(f"Last row (row {active_rows[-1][0]}): nom={active_rows[-1][1]}, saldo={active_rows[-1][2]}")
print(f"Saldo Akhir math: 2564938 + {pos_sum} + {neg_sum} = {2564938 + pos_sum + neg_sum}")
