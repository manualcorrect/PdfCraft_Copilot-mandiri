import os
import openpyxl
import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\okt"
EXCEL_PATH = os.path.join(BASE_DIR, "Template_Mutasi_OKT.xlsx")
PDF_PATH = os.path.join(BASE_DIR, "0.pdf")

wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)
ws = wb['Tabel_Mutasi']
excel_txs = []
for r in range(6, 100):
    nom = ws.cell(r, 5).value
    sal = ws.cell(r, 7).value
    if nom is not None and abs(float(nom)) > 0.001:
        excel_txs.append({
            'row': r,
            'nom': float(nom),
            'sal': float(sal),
            'desc': ws.cell(r, 4).value
        })

print(f"Total Excel txs: {len(excel_txs)}")

pdf_txs = []
with pdfplumber.open(PDF_PATH) as pdf:
    for p_idx, page in enumerate(pdf.pages):
        words = page.extract_words()
        # Find nominals around x=370..450
        min_top = 320 if p_idx == 0 else 200
        table_words = [w for w in words if min_top <= w['top'] <= 800]
        wibs = sorted([w for w in table_words if w['text'] == 'WIB'], key=lambda x: x['top'])
        for w in wibs:
            # find nominal near w['top']
            nom_words = [x for x in table_words if abs(x['top'] - w['top']) < 15 and 370 <= x['x0'] <= 455]
            nom_str = nom_words[0]['text'] if nom_words else 'NONE'
            sal_words = [x for x in table_words if abs(x['top'] - w['top']) < 15 and x['x0'] > 470]
            sal_str = sal_words[0]['text'] if sal_words else 'NONE'
            pdf_txs.append({
                'page': p_idx + 1,
                'top': w['top'],
                'nom_str': nom_str,
                'sal_str': sal_str
            })

print(f"Total PDF txs: {len(pdf_txs)}")

print("\nComparing Nominals (where they differ):")
differing_nominals = []
for i in range(min(len(excel_txs), len(pdf_txs))):
    ex = excel_txs[i]
    pdf_item = pdf_txs[i]
    # format excel nom
    is_cr = ex['nom'] > 0
    ex_nom_str = ("+" if is_cr else "-") + f"{abs(ex['nom']):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    if ex_nom_str != pdf_item['nom_str']:
        print(f"Tx #{i+1} (Row {ex['row']}, Page {pdf_item['page']}): Excel='{ex_nom_str}' vs PDF='{pdf_item['nom_str']}'")
        differing_nominals.append(i+1)

print(f"Total differing nominals: {len(differing_nominals)} -> {differing_nominals}")
