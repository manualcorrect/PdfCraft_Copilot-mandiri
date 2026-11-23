import pdfplumber
import openpyxl

okt_dir = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\okt"
pdf_path = f"{okt_dir}\\0.pdf"
xlsx_path = f"{okt_dir}\\Template_Mutasi_OKT.xlsx"

wb = openpyxl.load_workbook(xlsx_path, data_only=True)
ws_mutasi = wb["Tabel_Mutasi"]

excel_tx = []
for r in range(6, ws_mutasi.max_row + 1):
    c_nom = ws_mutasi.cell(r, 5).value
    c_saldo = ws_mutasi.cell(r, 7).value
    if c_nom is not None:
        excel_tx.append({
            'row': r,
            'nom': float(c_nom),
            'saldo': float(c_saldo) if c_saldo is not None else None
        })

print(f"Total rows in Excel with nominal: {len(excel_tx)}")

# Extract 0.pdf
pdf_tx = []
with pdfplumber.open(pdf_path) as pdf:
    for p_idx, page in enumerate(pdf.pages):
        words = page.extract_words()
        col_no = [w for w in words if 15 <= w['x0'] <= 35 and 150 <= w['top'] <= 800 and w['text'].isdigit()]
        col_no.sort(key=lambda w: w['top'])
        for w in col_no:
            amt_words = [aw for aw in words if 350 <= aw['x0'] <= 440 and abs(aw['top'] - w['top']) <= 5]
            amt_str = amt_words[0]['text'] if amt_words else '0'
            clean_amt = amt_str.replace('.', '').replace(',', '.').replace('+', '')
            pdf_tx.append({
                'page': p_idx + 1,
                'no': int(w['text']),
                'raw_amt': amt_str,
                'nom': float(clean_amt)
            })

print(f"Total tx in 0.pdf: {len(pdf_tx)}")

# Compare skipping rows 16 and 17 in Excel
excel_nonzero = [t for t in excel_tx if t['nom'] != 0 or t['row'] not in (16, 17)]
print(f"Excel non-zero / active: {len(excel_nonzero)}")

for i in range(min(len(pdf_tx), len(excel_nonzero))):
    p = pdf_tx[i]
    e = excel_nonzero[i]
    match = (p['nom'] == e['nom'])
    flag = "MATCH" if match else f"DIFF: PDF={p['nom']:,.2f} vs Excel={e['nom']:,.2f}"
    print(f"Index {i:2d} | P{p['page']} Tx {p['no']:3d} | Excel Row {e['row']:2d} | {flag}")
