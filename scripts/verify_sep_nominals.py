import openpyxl
import pdfplumber

excel_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\Template_Mutasi_SEP.xlsx"
pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf"

wb = openpyxl.load_workbook(excel_path, data_only=True)
ws = wb["Tabel_Mutasi"]
excel_noms = []
for r in range(6, 60):
    val = ws.cell(r, 5).value
    if val is not None and abs(val) > 0.001:
        excel_noms.append(float(val))

with pdfplumber.open(pdf_path) as pdf:
    pdf_noms = []
    for p_idx, page in enumerate(pdf.pages):
        words = page.extract_words()
        min_top = 320 if p_idx == 0 else 200
        table_words = [w for w in words if min_top <= w['top'] <= 800]
        wibs = sorted([w for w in table_words if w['text'] == 'WIB'], key=lambda x: x['top'])
        for w in wibs:
            nom_cands = [x for x in table_words if abs(x['top'] - w['top']) < 15 and 370 <= x['x0'] < 480]
            nom_str = " ".join([x['text'] for x in nom_cands]).replace(".", "").replace(",", ".")
            pdf_noms.append(float(nom_str))

print(f"Excel count: {len(excel_noms)}, PDF count: {len(pdf_noms)}")
diffs = []
for i in range(len(excel_noms)):
    e = excel_noms[i]
    p = pdf_noms[i]
    if abs(e - p) > 0.01:
        diffs.append((i+1, e, p))
        print(f"Diff Tx {i+1:2d}: Excel={e:>12,.2f} vs PDF={p:>12,.2f}")

print(f"Total nominal diffs: {len(diffs)}")
