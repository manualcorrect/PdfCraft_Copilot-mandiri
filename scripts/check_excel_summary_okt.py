import openpyxl

excel_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\okt\Template_Mutasi_OKT.xlsx"
wb = openpyxl.load_workbook(excel_path, data_only=True)
print("Sheet names:", wb.sheetnames)
ws = wb['Tabel_Mutasi']
for r in range(1, 10):
    vals = [ws.cell(r, c).value for c in range(1, 10)]
    print(f"Row {r}: {vals}")

# Check summary cells or info in the sheet or other sheets
for sheet in wb.sheetnames:
    s = wb[sheet]
    print(f"\nSheet {sheet}: max_row={s.max_row}, max_col={s.max_column}")
    for r in range(1, 10):
        row_vals = [s.cell(r, c).value for c in range(1, 8)]
        if any(v is not None for v in row_vals):
            print(f"  Row {r}: {row_vals}")
