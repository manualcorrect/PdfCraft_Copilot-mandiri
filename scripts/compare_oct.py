import pdfplumber
import openpyxl

pdf_p = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\1.pdf"
excel_p = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\Template_Mutasi.xlsx"

with pdfplumber.open(pdf_p) as pdf:
    pdf_txs = []
    for p_idx, page in enumerate(pdf.pages):
        words = page.extract_words()
        min_top = 320 if p_idx == 0 else 200
        table_words = [w for w in words if min_top <= w['top'] <= 800]
        wibs = sorted([w for w in table_words if w['text'] == 'WIB'], key=lambda x: x['top'])
        for w in wibs:
            noms = [x['text'] for x in table_words if abs(x['top'] - w['top']) < 15 and 370 <= x['x0'] <= 450]
            descs = [x['text'] for x in table_words if abs(x['top'] - w['top']) < 20 and 120 <= x['x0'] <= 360]
            pdf_txs.append({
                'page': p_idx + 1,
                'desc': ' '.join(descs)[:35],
                'nom': noms[0] if noms else 'N/A'
            })

wb = openpyxl.load_workbook(excel_p, data_only=True)
ws = wb['Tabel_Mutasi']
excel_txs = []
for r in range(6, ws.max_row + 1):
    nom = ws.cell(r, 5).value
    saldo = ws.cell(r, 7).value
    if nom is not None and str(nom).strip() != '':
        excel_txs.append({'row': r, 'nom': nom, 'saldo': saldo})

print(f"Total PDF txs: {len(pdf_txs)}")
print(f"Total Excel rows: {len(excel_txs)}")
for i in range(max(len(pdf_txs), len(excel_txs))):
    p_info = f"P{pdf_txs[i]['page']} {pdf_txs[i]['nom']:>14} | {pdf_txs[i]['desc']}" if i < len(pdf_txs) else "N/A"
    e_info = f"R{excel_txs[i]['row']} nom={excel_txs[i]['nom']} saldo={excel_txs[i]['saldo']:.2f}" if i < len(excel_txs) else "N/A"
    print(f"{i+1:2d}. PDF: {p_info:<55} || EXCEL: {e_info}")
