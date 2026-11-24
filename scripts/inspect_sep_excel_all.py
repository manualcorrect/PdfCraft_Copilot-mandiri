import openpyxl

wb = openpyxl.load_workbook(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\sep\Template_Mutasi_SEP.xlsx')
ws = wb['Tabel_Mutasi']

print(f"Max row: {ws.max_row}")
for r in range(5, 55):
    vals = [ws.cell(r, c).value for c in range(1, 9)]
    print(f"Row {r:2d}: {vals}")
