import openpyxl

xlsx_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\okt\Template_Mutasi_OKT.xlsx"
wb = openpyxl.load_workbook(xlsx_path, data_only=True)
ws_mutasi = wb["Tabel_Mutasi"]

print("Row 4 headers:")
print([ws_mutasi.cell(4, c).value for c in range(1, 15)])

print("\nRow 5 (Awal):")
print([ws_mutasi.cell(5, c).value for c in range(1, 15)])

print("\nRows 6 to 15:")
for r in range(6, 16):
    vals = [ws_mutasi.cell(r, c).value for c in range(1, 10)]
    print(f"Row {r}: {vals}")
