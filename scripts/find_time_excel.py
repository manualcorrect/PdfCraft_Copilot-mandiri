import openpyxl

excel_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\Template_Mutasi_Aug.xlsx"
wb = openpyxl.load_workbook(excel_path, data_only=True)
ws2 = wb["Tabel_Mutasi"]

for r in range(1, ws2.max_row + 1):
    for c in range(1, ws2.max_column + 1):
        v = ws2.cell(r, c).value
        if v and any(k in str(v) for k in ["04:00", "WIB", "2026"]):
            print(f"Cell ({r}, {c}) [{ws2.cell(4, c).value}]: {repr(v)}")
