import openpyxl

wb = openpyxl.load_workbook(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\Template_Mutasi_AUG.xlsx", data_only=True)
ws_hr = wb['Header & Ringkasan']
print("Header & Ringkasan:")
for r in range(1, 30):
    val_a = ws_hr.cell(r, 1).value
    val_b = ws_hr.cell(r, 2).value
    if val_a or val_b:
        print(f"Row {r}: A='{val_a}' | B='{val_b}'")

ws_tm = wb['Tabel_Mutasi']
print("\nTabel_Mutasi Rows 1-10:")
for r in range(1, 10):
    vals = [ws_tm.cell(r, c).value for c in range(1, 9)]
    print(f"Row {r}: {vals}")
