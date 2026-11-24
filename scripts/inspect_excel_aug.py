import openpyxl

wb = openpyxl.load_workbook(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\aug\Template_Mutasi_AUG.xlsx')
ws = wb['Tabel_Mutasi']
for r in range(25, ws.max_row + 1):
    vals = [ws.cell(r, c).value for c in range(1, 9)]
    if any(vals):
        print(f"Row {r:2d}: {vals}")
