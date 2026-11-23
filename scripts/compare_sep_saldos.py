import openpyxl
import pdfplumber

excel_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\Template_Mutasi_SEP.xlsx"
pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf"

wb = openpyxl.load_workbook(excel_path, data_only=True)
ws = wb["Tabel_Mutasi"]

excel_rows = []
for r in range(6, 60):
    nom = ws.cell(r, 5).value
    sal = ws.cell(r, 7).value
    if nom is not None and abs(nom) > 0.001:
        excel_rows.append({
            'excel_row': r,
            'nom': float(nom),
            'saldo': float(sal) + 0.81
        })

print(f"Total active Excel rows: {len(excel_rows)}")

def fmt(n):
    return f"{abs(n):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

for i, er in enumerate(excel_rows):
    print(f"Tx {i+1:2d} (Excel R{er['excel_row']:2d}): Nom={fmt(er['nom']):>14} Saldo={fmt(er['saldo']):>14}")
