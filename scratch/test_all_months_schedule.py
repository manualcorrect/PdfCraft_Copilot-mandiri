import sys, openpyxl, pdfplumber
sys.path.insert(0, 'src')
from smart_date_time_generator import shuffle_and_synchronize_schedule

months_data = [
    ('AUG', r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\REK_GALANG_AUG_2026_PERFECT.pdf', r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\Template_Mutasi_Aug.xlsx', 8, 22, 31),
    ('SEP', r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_SEP_2026_PERFECT.pdf', r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\Template_Mutasi_SEP_Reconciled.xlsx', 9, 22, 30),
    ('OCT', r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\REK_GALANG_OCT_2026_PERFECT.pdf', r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\Template_Mutasi_OCT_Reconciled.xlsx', 10, 27, 31)
]

for m_code, pdf_p, xls_p, m_num, sal_no, last_d in months_data:
    wb = openpyxl.load_workbook(xls_p, data_only=True)
    ws = wb['Tabel_Mutasi']
    txs = []
    with pdfplumber.open(pdf_p) as pdf:
        items = []
        for p_idx, page in enumerate(pdf.pages):
            words = page.extract_words()
            min_top = 320 if p_idx == 0 else 200
            table_words = [w for w in words if min_top <= w['top'] <= 800]
            wibs = sorted([w for w in table_words if w['text'] == 'WIB'], key=lambda x: x['top'])
            for ww in wibs:
                time_w = [w['text'] for w in table_words if abs(w['top'] - ww['top']) < 3 and w['x1'] <= ww['x0'] + 1]
                t_str = f"{time_w[-1]} WIB" if time_w else "12:00:00 WIB"
                date_w = [w['text'] for w in table_words if 0 < (ww['top'] - w['top']) < 15 and 45 <= w['x0'] <= 90]
                d_str = " ".join(date_w).strip()
                desc_words = sorted([w for w in table_words if abs(w['top'] - ww['top']) < 22 and 115 <= w['x0'] <= 365], key=lambda x: (x['top'], x['x0']))
                lines = []
                curr_l = []
                curr_y = None
                for w in desc_words:
                    if curr_y is None or abs(w['top'] - curr_y) < 4:
                        curr_l.append(w['text'])
                        curr_y = w['top'] if curr_y is None else (curr_y * 0.7 + w['top'] * 0.3)
                    else:
                        lines.append(' '.join(curr_l))
                        curr_l = [w['text']]
                        curr_y = w['top']
                if curr_l:
                    lines.append(' '.join(curr_l))
                desc_text = '\n'.join(lines)
                items.append({'date': d_str, 'time': t_str, 'desc': desc_text})

    # Read nominals from Excel
    row_idx = 0
    for r in range(6, ws.max_row + 1):
        nom_cell = ws.cell(r, 5).value
        sal_cell = ws.cell(r, 7).value
        if nom_cell is None or str(nom_cell).strip() == '':
            continue
        nom = float(str(nom_cell).replace("Rp", "").replace(".", "").replace(",", ".").strip())
        sal = float(str(sal_cell).replace("Rp", "").replace(".", "").replace(",", ".").strip())
        
        auth = items[row_idx] if row_idx < len(items) else {'date': f'01 {m_code} 2026', 'time': '12:00:00 WIB', 'desc': '-'}
        txs.append({
            'no': row_idx + 1,
            'date': auth['date'],
            'time': auth['time'],
            'desc': auth['desc'],
            'nom_num': nom,
            'saldo_num': sal
        })
        row_idx += 1

    shuffled = shuffle_and_synchronize_schedule(txs, m_num, 2026, salary_no=sal_no, last_day=last_d)
    print(f"\n==================== {m_code} SCHEDULE VERIFICATION ====================")
    print(f"Total transactions: {len(shuffled)} | Salary at No {sal_no}")
    print("--- Sample Pre-Gaji (Rows 1-5): ---")
    for t in shuffled[:5]:
        print(f"  No {t['no']:2d}: {t['date']} | {t['time']} | {t['desc'][:30]}")
    print(f"--- Salary Transaction (No {sal_no}): ---")
    sal_t = [t for t in shuffled if t['no'] == sal_no][0]
    print(f"  No {sal_t['no']:2d}: {sal_t['date']} | {sal_t['time']} | {sal_t['desc'][:30]}")
    print("--- Sample Post-Gaji (Last 5 Rows): ---")
    for t in shuffled[-5:]:
        print(f"  No {t['no']:2d}: {t['date']} | {t['time']} | {t['desc'][:30]}")
