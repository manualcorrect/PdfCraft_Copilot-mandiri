import openpyxl

wb = openpyxl.load_workbook(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\aug\Template_Mutasi_AUG.xlsx')
ws = wb['Tabel_Mutasi']
for r in [29, 38, 39]:
    print(f"Row {r:2d}: No={ws.cell(r, 1).value}, Tgl={ws.cell(r, 2).value}, Jam={ws.cell(r, 3).value}, Ket={repr(ws.cell(r, 4).value)}, Nom={ws.cell(r, 5).value}, Saldo={ws.cell(r, 7).value}")
