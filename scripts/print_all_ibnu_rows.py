import openpyxl
import pdfplumber

excel_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\Template_Mutasi_AUG.xlsx"
pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\0.pdf"

wb = openpyxl.load_workbook(excel_path, data_only=True)
ws = wb['Tabel_Mutasi']

excel_noms = []
for r in range(6, ws.max_row + 1):
    nom = ws.cell(r, 5).value
    saldo = ws.cell(r, 7).value
    if nom is not None or saldo is not None:
        excel_noms.append((r, nom, saldo))

pdf_noms = []
with pdfplumber.open(pdf_path) as pdf:
    for p_idx, page in enumerate(pdf.pages):
        words = page.extract_words()
        min_top = 310 if p_idx == 0 else 180
        wibs = sorted([w for w in words if min_top <= w['top'] <= 780 and w['text'] == 'WIB'], key=lambda w: w['top'])
        for w in wibs:
            r_words = [x for x in words if abs(x['top'] - w['top']) < 15]
            n_candidates = [x for x in r_words if 360 <= x['x0'] <= 430 and (x['text'].startswith('+') or x['text'].startswith('-'))]
            nom_str = n_candidates[0]['text'] if n_candidates else ''
            pdf_noms.append((p_idx + 1, nom_str))

print("=== ALL EXCEL ROWS ===")
for idx, (r, nom, saldo) in enumerate(excel_noms):
    p_info = pdf_noms[idx] if idx < len(pdf_noms) else ('NO_PDF', 'NO_PDF')
    print(f"Idx {idx+1:2d} (Row {r:2d}): Nom={nom:<10} Saldo={saldo:<10} | PDF: p{p_info[0]} Nom={p_info[1]}")
