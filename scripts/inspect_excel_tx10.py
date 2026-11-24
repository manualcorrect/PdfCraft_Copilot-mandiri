import openpyxl

wb = openpyxl.load_workbook(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\sep\Template_Mutasi_SEP.xlsx')
ws = wb['Tabel_Mutasi']

for r in range(12, 20):
    row_vals = [ws.cell(r, c).value for c in range(1, 9)]
    print(f"Row {r:2d}: {row_vals}")
