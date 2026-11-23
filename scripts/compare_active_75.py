import openpyxl
import pdfplumber
import re

excel_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\Template_Mutasi_AUG.xlsx"
pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\0.pdf"

wb = openpyxl.load_workbook(excel_path, data_only=True)
ws = wb['Tabel_Mutasi']

excel_txs = []
for r in range(6, ws.max_row + 1):
    nom = ws.cell(r, 5).value
    saldo = ws.cell(r, 7).value
    if nom is not None and abs(float(nom)) > 0.001:
        excel_txs.append({
            'row': r,
            'nom': float(nom),
            'saldo': float(saldo)
        })

print(f"Active Excel transactions: {len(excel_txs)}")

pdf_txs = []
with pdfplumber.open(pdf_path) as pdf:
    for p_idx, page in enumerate(pdf.pages):
        words = page.extract_words()
        min_top = 310 if p_idx == 0 else 180
        t_words = [w for w in words if min_top <= w['top'] <= 780]
        wibs = sorted([w for w in t_words if w['text'] == 'WIB'], key=lambda x: x['top'])
        for w in wibs:
            y = w['top']
            # nominal
            noms = [x for x in t_words if abs(x['top'] - y) < 15 and 360 <= x['x0'] <= 440 and ('+' in x['text'] or '-' in x['text'])]
            nom_str = noms[0]['text'] if noms else "NONE"
            # saldo
            sals = [x for x in t_words if abs(x['top'] - y) < 15 and 500 <= x['x0'] <= 580 and ',' in x['text']]
            sal_str = sals[0]['text'] if sals else "NONE"
            # no
            nos = [x for x in t_words if abs(x['top'] - y) < 15 and 15 <= x['x0'] <= 35]
            no_str = nos[0]['text'] if nos else "NONE"
            pdf_txs.append({
                'page': p_idx + 1,
                'no': no_str,
                'nom_str': nom_str,
                'sal_str': sal_str
            })

print(f"PDF transactions: {len(pdf_txs)}")

diffs = []
for i in range(75):
    e = excel_txs[i]
    p = pdf_txs[i]
    # parse pdf nom
    p_nom_val = float(p['nom_str'].replace('.', '').replace(',', '.').replace(' ', '').replace('+', ''))
    if abs(e['nom'] - p_nom_val) > 0.01:
        diffs.append((i+1, e['row'], e['nom'], p['page'], p['no'], p['nom_str']))

print(f"\nTotal nominal differences when skipping dummy rows: {len(diffs)}")
for d in diffs:
    print(f"Tx {d[0]:02d} (Excel Row {d[1]}): Excel={d[2]:>12,.2f} | PDF (P{d[3]} No {d[4]}): {d[5]}")
