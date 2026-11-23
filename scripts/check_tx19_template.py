import openpyxl

excel_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\Template_Mutasi_Aug.xlsx"
wb = openpyxl.load_workbook(excel_path, data_only=True)
ws2 = wb["Tabel_Mutasi"]

print("--- Inspecting Tabel_Mutasi rows 15 to 30 ---")
for r in range(15, 30):
    vals = [ws2.cell(r, c).value for c in range(1, 8)]
    print(f"Excel Row {r:02d}: {vals}")
