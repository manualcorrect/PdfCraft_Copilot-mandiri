import openpyxl

excel_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\Template_Mutasi_Aug.xlsx"
wb = openpyxl.load_workbook(excel_path, data_only=True)
ws2 = wb["Tabel_Mutasi"]

print("User Excel rows:")
for r in range(6, 20):
    no = ws2.cell(r, 1).value
    tgl = ws2.cell(r, 2).value
    uraian = ws2.cell(r, 3).value
    nom = ws2.cell(r, 5).value
    print(f"Row {r:02d}: No={no}, Tgl={tgl}, Nom={nom}, Uraian={repr(uraian)[:30]}")
