import openpyxl
import pdfplumber

excel_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\Template_Mutasi_AUG.xlsx"
pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\0.pdf"

wb = openpyxl.load_workbook(excel_path, data_only=True)
ws = wb['Tabel_Mutasi']

excel_rows = []
for r in range(6, ws.max_row + 1):
    nom = ws.cell(r, 5).value
    saldo = ws.cell(r, 7).value
    if nom is not None or saldo is not None:
        excel_rows.append({
            'row': r,
            'tx_no': len(excel_rows) + 1,
            'no': ws.cell(r, 1).value,
            'tgl': ws.cell(r, 2).value,
            'jam': ws.cell(r, 3).value,
            'ket': ws.cell(r, 4).value,
            'nom': nom,
            'saldo': saldo
        })

print(f"Total excel transaction rows: {len(excel_rows)}")

# Extract all 0.pdf transactions
pdf_txs = []
with pdfplumber.open(pdf_path) as pdf:
    for p_idx, page in enumerate(pdf.pages):
        words = page.extract_words()
        min_top = 310 if p_idx == 0 else 180
        # group by row by looking at WIB
        wibs = sorted([w for w in words if min_top <= w['top'] <= 780 and w['text'] == 'WIB'], key=lambda w: w['top'])
        for w in wibs:
            # find words within +/- 15 pt of w['top']
            r_words = [x for x in words if abs(x['top'] - w['top']) < 15]
            # find nominal
            n_candidates = [x for x in r_words if 360 <= x['x0'] <= 430 and (x['text'].startswith('+') or x['text'].startswith('-'))]
            nom_str = n_candidates[0]['text'] if n_candidates else ''
            # find saldo
            s_candidates = [x for x in r_words if 500 <= x['x0'] <= 570 and ',' in x['text']]
            saldo_str = s_candidates[0]['text'] if s_candidates else ''
            # find date
            d_candidates = [x for x in r_words if 45 <= x['x0'] <= 95 and x['top'] < w['top']]
            d_candidates.sort(key=lambda x: x['x0'])
            d_str = " ".join([x['text'] for x in d_candidates])
            # find time
            t_candidates = [x for x in r_words if abs(x['top'] - w['top']) < 3 and x['x1'] <= w['x0'] + 1]
            time_str = f"{t_candidates[-1]['text']} WIB" if t_candidates else ''
            # find no
            no_candidates = [x for x in r_words if 15 <= x['x0'] <= 35]
            no_str = no_candidates[0]['text'] if no_candidates else ''
            
            pdf_txs.append({
                'page': p_idx + 1,
                'no': no_str,
                'date': d_str,
                'time': time_str,
                'nom': nom_str,
                'saldo': saldo_str,
                'top': w['top']
            })

print(f"Total 0.pdf transactions: {len(pdf_txs)}")

print("\n--- COMPARISON FIRST 15 ROWS ---")
for i in range(min(15, len(excel_rows))):
    e = excel_rows[i]
    p = pdf_txs[i] if i < len(pdf_txs) else {}
    print(f"Tx {i+1:2d} | Excel: Nom={e['nom']} Saldo={e['saldo']} | PDF: p{p.get('page')} No={p.get('no')} Nom={p.get('nom')} Saldo={p.get('saldo')}")

print("\n--- CHECKING ROWS WHERE NOMINALS DIFFER ---")
diff_count = 0
for i in range(min(len(excel_rows), len(pdf_txs))):
    e = excel_rows[i]
    p = pdf_txs[i]
    # parse pdf nom
    p_nom_clean = p['nom'].replace('.', '').replace(',', '.').replace(' ', '')
    try:
        p_nom_val = float(p_nom_clean)
    except:
        p_nom_val = None
    
    if p_nom_val is not None and abs(p_nom_val - e['nom']) > 0.01:
        diff_count += 1
        if diff_count <= 10:
            print(f"Diff at Tx {i+1}: Excel={e['nom']} vs PDF={p['nom']} (p{p['page']} No={p['no']})")

print(f"Total nominal differences: {diff_count}")
