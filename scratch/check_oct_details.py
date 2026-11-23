import openpyxl, pdfplumber

excel_path = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\Template_Mutasi_OCT_Reconciled.xlsx'
wb = openpyxl.load_workbook(excel_path, data_only=True)
ws2 = wb['Tabel_Mutasi']
rows = []
for r in range(5, ws2.max_row + 1):
    no = ws2.cell(r, 1).value
    nom = ws2.cell(r, 5).value
    sal = ws2.cell(r, 7).value
    if nom is not None and str(nom).strip() != '':
        rows.append((r, no, ws2.cell(r, 2).value, ws2.cell(r, 3).value, nom, sal))

print(f"Excel OCT total rows with nominal: {len(rows)}")
for ro in rows:
    if ro[1] == '[AWAL]' or ro[1] is None or int(ro[1]) in [1, 2, 26, 27, 34, 35, 36, 37, 38]:
        print(ro)

pdf_path = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\REK_GALANG_OCT_2026_PERFECT.pdf'
with pdfplumber.open(pdf_path) as pdf:
    print(f"PDF Pages: {len(pdf.pages)}")
    for p_idx, page in enumerate(pdf.pages):
        words = page.extract_words()
        wibs = [w for w in words if w['text'] == 'WIB']
        print(f"  Page {p_idx+1}: {len(wibs)} WIB items")
