import pdfplumber, re

with pdfplumber.open(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\sep\0.pdf') as pdf:
    pdf_tx_meta = []
    for p_idx in range(4):
        page = pdf.pages[p_idx]
        words = page.extract_words()
        min_top = 310 if p_idx == 0 else 180
        t_words = [w for w in words if min_top <= w['top'] <= 780]
        wibs = sorted([w for w in t_words if w['text'] == 'WIB'], key=lambda x: x['top'])
        for r_i, w in enumerate(wibs):
            t_candidates = [x for x in t_words if abs(x['top'] - w['top']) < 3 and x['x1'] <= w['x0'] + 1]
            time_str = f"{t_candidates[-1]['text']} WIB" if t_candidates else '12:00:00 WIB'
            d_candidates = [x for x in t_words if 0 < (w['top'] - x['top']) < 15 and 45 <= x['x0'] <= 95]
            d_candidates.sort(key=lambda x: x['x0'])
            d_str = " ".join([x['text'] for x in d_candidates])
            m = re.search(r'^(\d+)', d_str)
            day_num = int(m.group(1)) if m else 1
            pdf_tx_meta.append({
                'tx_idx': len(pdf_tx_meta) + 1,
                'page': p_idx + 1,
                'row': r_i + 1,
                'orig_day': day_num,
                'orig_time': time_str,
                'orig_date': d_str
            })

print(f"Total extracted: {len(pdf_tx_meta)}")
for meta in pdf_tx_meta:
    print(f"Tx {meta['tx_idx']:2d} (P{meta['page']} R{meta['row']:2d}): Day={meta['orig_day']:2d} | Time={meta['orig_time']:<12} | Date='{meta['orig_date']}'")
