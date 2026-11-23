import os
import openpyxl
import pdfplumber

BASE_DIR = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\okt"
EXCEL_PATH = os.path.join(BASE_DIR, "Template_Mutasi_OKT.xlsx")
PDF_PATH = os.path.join(BASE_DIR, "0.pdf")

print("Checking Excel...")
wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)
ws = wb['Tabel_Mutasi']
rows = []
for r in range(6, 100):
    nom = ws.cell(r, 5).value
    sal = ws.cell(r, 7).value
    desc = ws.cell(r, 4).value
    if nom is not None and abs(float(nom)) > 0.001:
        rows.append((r, nom, sal, desc))

print(f"Total active rows in Excel: {len(rows)}")
for idx, (r, nom, sal, desc) in enumerate(rows):
    if abs(float(nom) - 6903611.0) < 1.0 or idx in [0, 1, len(rows)-2, len(rows)-1]:
        print(f"Row {r} (tx #{idx+1}): nom={nom}, sal={sal}, desc={desc}")

print("\nChecking 0.pdf...")
with pdfplumber.open(PDF_PATH) as pdf:
    print(f"Total pages in 0.pdf: {len(pdf.pages)}")
    for p_idx, page in enumerate(pdf.pages):
        words = page.extract_words()
        wibs = [w for w in words if w['text'] == 'WIB']
        print(f"Page {p_idx+1}: {len(wibs)} WIB occurrences (transactions)")
