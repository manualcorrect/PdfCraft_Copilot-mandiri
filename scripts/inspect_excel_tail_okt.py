import openpyxl

wb = openpyxl.load_workbook(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\okt\Template_Mutasi_OKT.xlsx')
ws = wb['Tabel_Mutasi']
for r in range(46, 53):
    vals = [ws.cell(r, c).value for c in range(1, 9)]
    print(f"Row {r:2d}: {vals}")
