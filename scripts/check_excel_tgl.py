import openpyxl

wb = openpyxl.load_workbook("templates/Template_Mutasi_Aug_Reconciled.xlsx", data_only=True)
ws2 = wb["Tabel_Mutasi"]

print("Excel rows:")
for r in range(6, 20):
    no = ws2.cell(r, 1).value
    tgl = ws2.cell(r, 2).value
    uraian = ws2.cell(r, 3).value
    nom = ws2.cell(r, 5).value
    print(f"Row {r:02d}: No={no}, Tgl={tgl}, Nom={nom}, Uraian={repr(uraian)[:30]}")
