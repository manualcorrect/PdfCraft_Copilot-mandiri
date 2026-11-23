import openpyxl

src_p = "output/Template_Mutasi_SEP_Reconciled.xlsx"
out_p = "output/Template_Mutasi_SEP_Recommended.xlsx"

wb = openpyxl.load_workbook(src_p)
ws2 = wb["Tabel_Mutasi"]

# Update rows 15, 16, 17
# Row 15: nom = -1000, saldo = 3200847.81
ws2.cell(15, 5).value = -1000
ws2.cell(15, 7).value = 3200847.81

# Row 16: nom = -658000, saldo = 2542847.81
ws2.cell(16, 5).value = -658000
ws2.cell(16, 7).value = 2542847.81

# Row 17: nom = -1000, saldo = 2541847.81
ws2.cell(17, 5).value = -1000
ws2.cell(17, 7).value = 2541847.81

wb.save(out_p)
print("Saved Template_Mutasi_SEP_Recommended.xlsx!")
