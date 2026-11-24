import openpyxl

wb = openpyxl.load_workbook(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\okt\Template_Mutasi_OKT.xlsx')
ws = wb['Tabel_Mutasi']

non_zero_rows = []
for r in range(6, ws.max_row + 1):
    nom = ws.cell(r, 5).value
    saldo = ws.cell(r, 7).value
    tgl = ws.cell(r, 2).value
    jam = ws.cell(r, 3).value
    desc = ws.cell(r, 4).value
    if nom is not None and abs(float(nom)) > 0.001:
        non_zero_rows.append((r, nom, saldo, tgl, jam, desc))

print(f"Total active transactions: {len(non_zero_rows)}")
for idx, (r, nom, saldo, tgl, jam, desc) in enumerate(non_zero_rows):
    print(f"Tx {idx+1:2d} (Row {r:2d}): Nom={nom:>12} | Saldo={saldo} | Tgl={tgl} | Jam={jam} | Desc={repr(desc)}")
