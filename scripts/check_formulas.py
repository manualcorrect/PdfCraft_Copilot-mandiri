import openpyxl

excel_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\Template_Mutasi_AUG.xlsx"
wb_formulas = openpyxl.load_workbook(excel_path, data_only=False)
ws_f = wb_formulas['Header & Ringkasan']

for r in range(21, 27):
    print(f"Row {r}: B={repr(ws_f.cell(r, 2).value)}, C={repr(ws_f.cell(r, 3).value)}, D={repr(ws_f.cell(r, 4).value)}")
