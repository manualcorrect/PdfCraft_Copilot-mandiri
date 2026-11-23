import openpyxl

excel_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\Template_Mutasi_Aug.xlsx"
wb = openpyxl.load_workbook(excel_path, data_only=True)
for sheet in wb.sheetnames:
    ws = wb[sheet]
    print(f"=== Sheet: {sheet} (max_row={ws.max_row}, max_col={ws.max_column}) ===")
    for r in range(1, min(ws.max_row+1, 25)):
        row_vals = [ws.cell(r, c).value for c in range(1, min(ws.max_column+1, 10))]
        if any(v is not None for v in row_vals):
            print(f"  Row {r:02d}: {row_vals}")
