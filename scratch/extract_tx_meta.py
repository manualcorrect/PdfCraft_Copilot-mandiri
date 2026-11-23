import sys, re, datetime, openpyxl, pdfplumber
sys.path.insert(0, 'src')

excel_path = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\Template_Mutasi_AUG.xlsx'
pdf_path = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf'

wb = openpyxl.load_workbook(excel_path, data_only=True)
ws = wb['Tabel_Mutasi']

excel_txs = []
for r in range(6, 64):
    nom = ws.cell(r, 5).value
    bal = ws.cell(r, 7).value
    d_val = ws.cell(r, 2).value
    t_val = ws.cell(r, 3).value
    excel_txs.append({
        'row': r,
        'nom': float(nom),
        'saldo': float(bal),
        'date_in': str(d_val).strip() if d_val else None,
        'time_in': str(t_val).strip() if t_val else None
    })

print(f'Total excel txs: {len(excel_txs)}')

# Extract all 58 transactions from 0.pdf with their original date, time, and coords
pdf_tx_meta = []
with pdfplumber.open(pdf_path) as pdf:
    for p_idx in range(5):
        page = pdf.pages[p_idx]
        words = page.extract_words()
        min_top = 320 if p_idx == 0 else 200
        table_words = [w for w in words if min_top <= w['top'] <= 800]
        # Find all WIB words
        wibs = sorted([w for w in table_words if w['text'] == 'WIB'], key=lambda x: x['top'])
        for w in wibs:
            # find time word immediately to the left of WIB
            t_candidates = [x for x in table_words if abs(x['top'] - w['top']) < 3 and x['x1'] <= w['x0'] + 1]
            time_str = f"{t_candidates[-1]['text']} WIB" if t_candidates else "12:00:00 WIB"
            
            # find date words right above the time word (45 <= x0 <= 95)
            d_candidates = [x for x in table_words if 0 < (w['top'] - x['top']) < 15 and 45 <= x['x0'] <= 95]
            d_candidates.sort(key=lambda x: x['x0'])
            raw_d = " ".join([x['text'] for x in d_candidates]).strip()
            m = re.search(r'^(\d+)', raw_d)
            day_num = int(m.group(1)) if m else 1
            
            # find row number (No) near x0=20
            no_candidates = [x for x in table_words if abs(x['top'] - w['top']) < 12 and 18 <= x['x0'] <= 35]
            no_str = no_candidates[0]['text'] if no_candidates else str(len(pdf_tx_meta) + 1)
            
            # find nominal word near x1=432
            nom_c = [x for x in table_words if abs(x['top'] - w['top']) < 12 and 370 <= x['x0'] and x['x1'] <= 435]
            nom_str = nom_c[0]['text'] if nom_c else ""
            
            # find saldo word near x1=571
            sal_c = [x for x in table_words if abs(x['top'] - w['top']) < 12 and 500 <= x['x0'] and x['x1'] <= 575]
            sal_str = sal_c[0]['text'] if sal_c else ""

            pdf_tx_meta.append({
                'page': p_idx + 1,
                'no': int(no_str) if no_str.isdigit() else len(pdf_tx_meta) + 1,
                'orig_day': day_num,
                'orig_date_str': raw_d,
                'orig_time_str': time_str,
                'orig_nom_str': nom_str,
                'orig_sal_str': sal_str,
                'wib_top': w['top']
            })

print(f'Total PDF txs extracted: {len(pdf_tx_meta)}')
for i in range(5):
    print(f"Tx {i+1}: No={pdf_tx_meta[i]['no']} Date={pdf_tx_meta[i]['orig_date_str']} Time={pdf_tx_meta[i]['orig_time_str']} Nom={pdf_tx_meta[i]['orig_nom_str']}")
print("...")
for i in range(53, 58):
    print(f"Tx {i+1}: No={pdf_tx_meta[i]['no']} Date={pdf_tx_meta[i]['orig_date_str']} Time={pdf_tx_meta[i]['orig_time_str']} Nom={pdf_tx_meta[i]['orig_nom_str']}")
