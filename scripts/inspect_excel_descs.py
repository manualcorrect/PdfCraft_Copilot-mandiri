import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('templates/Galang_Jul_2026.xlsx', data_only=True)
ws = wb['Tabel_Mutasi']

print("=== Descriptions in Galang_Jul_2026.xlsx ===")
for r in range(6, 28):
    no = ws.cell(row=r, column=1).value
    desc = ws.cell(row=r, column=4).value
    print(f"Row {r-5:2d} (No {no}): {repr(desc)}")
