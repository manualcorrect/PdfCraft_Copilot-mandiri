import openpyxl

excel_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\Template_Mutasi_SEP_Reconciled.xlsx"

wb = openpyxl.load_workbook(excel_path, data_only=True)
print("Sheet names:", wb.sheetnames)
ws2 = wb["Tabel_Mutasi"]
print("Tabel_Mutasi rows count:", ws2.max_row)
for r in range(5, 15):
    row_vals = [ws2.cell(r, c).value for c in range(1, 8)]
    print(f"Row {r:2d}: {row_vals}")
