import openpyxl
import pdfplumber

excel_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\sep\Template_Mutasi_SEP.xlsx"
pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\sep\0.pdf"

wb = openpyxl.load_workbook(excel_path, data_only=True)
ws = wb['Tabel_Mutasi']

excel_txs = []
for r in range(6, 88):
    nom = ws.cell(r, 5).value
    saldo = ws.cell(r, 7).value
    ket = ws.cell(r, 4).value
    no = ws.cell(r, 1).value
    excel_txs.append({
        'row': r,
        'no': no,
        'nom': float(nom) if nom is not None else 0.0,
        'saldo': float(saldo) if saldo is not None else 0.0,
        'ket': ket
    })

print(f"Excel transactions count: {len(excel_txs)}")

pdf_txs = []
with pdfplumber.open(pdf_path) as pdf:
    for p_idx in range(7):  # pages 1..7
        page = pdf.pages[p_idx]
        words = page.extract_words()
        min_top = 310 if p_idx == 0 else 180
        t_words = [w for w in words if min_top <= w['top'] <= 780]
        wibs = sorted([w for w in t_words if w['text'] == 'WIB'], key=lambda x: x['top'])
        for w in wibs:
            y = w['top']
            # nominal
            noms = [x for x in t_words if abs(x['top'] - y) < 15 and 360 <= x['x0'] <= 450 and ('+' in x['text'] or '-' in x['text'])]
            nom_str = noms[0]['text'] if noms else "NONE"
            # saldo
            sals = [x for x in t_words if abs(x['top'] - y) < 15 and 500 <= x['x0'] <= 580 and ',' in x['text']]
            sal_str = sals[0]['text'] if sals else "NONE"
            # no
            nos = [x for x in t_words if abs(x['top'] - y) < 15 and 15 <= x['x0'] <= 35]
            no_str = nos[0]['text'] if nos else "NONE"
            # date
            dates = [x for x in t_words if 0 < (y - x['top']) < 18 and 45 <= x['x0'] <= 95]
            d_str = " ".join(x['text'] for x in sorted(dates, key=lambda x: x['x0']))
            # time
            t_candidates = [x for x in t_words if abs(x['top'] - y) < 3 and x['x1'] <= w['x0'] + 1]
            time_str = f"{t_candidates[-1]['text']} WIB" if t_candidates else '12:00:00 WIB'
            pdf_txs.append({
                'page': p_idx + 1,
                'no': no_str,
                'date': d_str,
                'time': time_str,
                'nom_str': nom_str,
                'sal_str': sal_str
            })

print(f"PDF transactions count: {len(pdf_txs)}")

diffs = []
for i in range(82):
    e = excel_txs[i]
    p = pdf_txs[i]
    p_nom_val = float(p['nom_str'].replace('.', '').replace(',', '.').replace(' ', '').replace('+', ''))
    if abs(e['nom'] - p_nom_val) > 0.01:
        diffs.append((i+1, e['row'], e['nom'], p['page'], p['no'], p['nom_str'], p['date'], p['time']))

print(f"\nNominal differences count: {len(diffs)}")
for d in diffs:
    print(f"Tx {d[0]:02d} (Row {d[1]}): Excel={d[2]:>12,.2f} | PDF P{d[3]} No {d[4]}: {d[5]:<15} (Orig: {d[6]} {d[7]})")
