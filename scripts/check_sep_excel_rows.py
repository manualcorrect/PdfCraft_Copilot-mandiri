import openpyxl

wb = openpyxl.load_workbook(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\sep\Template_Mutasi_SEP.xlsx')
ws = wb['Tabel_Mutasi']

non_zero_rows = []
for r in range(6, ws.max_row + 1):
    nom = ws.cell(r, 5).value
    saldo = ws.cell(r, 7).value
    if nom is not None and abs(float(nom)) > 0.001:
        non_zero_rows.append((r, nom, saldo))

print(f"Total non-zero nominal rows: {len(non_zero_rows)}")
for idx, (r, nom, saldo) in enumerate(non_zero_rows):
    print(f"Tx {idx+1:2d} (Excel row {r:3d}): Nom={nom:>12}, Saldo={saldo}")
