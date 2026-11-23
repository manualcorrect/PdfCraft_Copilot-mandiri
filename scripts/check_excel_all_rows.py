import pdfplumber
import openpyxl

okt_dir = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\okt"
pdf_path = f"{okt_dir}\\0.pdf"
xlsx_path = f"{okt_dir}\\Template_Mutasi_OKT.xlsx"

wb = openpyxl.load_workbook(xlsx_path, data_only=True)
ws_mutasi = wb["Tabel_Mutasi"]

excel_rows = []
for r in range(5, ws_mutasi.max_row + 1):
    vals = [ws_mutasi.cell(r, c).value for c in range(1, 8)]
    if any(v is not None for v in vals):
        excel_rows.append((r, vals))

print(f"Total non-empty rows in Tabel_Mutasi starting at row 5: {len(excel_rows)}")
for r, vals in excel_rows:
    print(f"Row {r:3d}: {vals}")
