import openpyxl

xlsx_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\okt\Template_Mutasi_OKT.xlsx"
wb = openpyxl.load_workbook(xlsx_path, data_only=True)
ws_mutasi = wb["Tabel_Mutasi"]

for r in range(5, ws_mutasi.max_row + 1):
    c_date = ws_mutasi.cell(r, 2).value
    c_time = ws_mutasi.cell(r, 3).value
    c_nom = ws_mutasi.cell(r, 5).value
    if c_date is not None or c_time is not None:
        print(f"Row {r:2d}: Date={c_date} | Time={c_time} | Nom={c_nom}")
