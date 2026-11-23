import openpyxl

excel_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\okt\Template_Mutasi_OKT.xlsx"
wb = openpyxl.load_workbook(excel_path, data_only=True)
ws = wb['Header & Ringkasan']
for r in range(10, 35):
    vals = [ws.cell(r, c).value for c in range(1, 6)]
    if any(v is not None for v in vals):
        print(f"Row {r:02d}: {vals}")
