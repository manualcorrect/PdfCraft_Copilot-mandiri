import pdfplumber
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\okt\0.pdf"

tx_meta = []
with pdfplumber.open(pdf_path) as pdf:
    for p_idx, page in enumerate(pdf.pages):
        words = page.extract_words()
        min_top = 320 if p_idx == 0 else 200
        table_words = [w for w in words if min_top <= w['top'] <= 800]
        wibs = sorted([w for w in table_words if w['text'] == 'WIB'], key=lambda x: x['top'])
        for w in wibs:
            t_cand = [x for x in table_words if abs(x['top'] - w['top']) < 3 and x['x1'] <= w['x0'] + 1]
            time_str = f"{t_cand[-1]['text']} WIB" if t_cand else '12:00:00 WIB'
            d_cand = [x for x in table_words if 0 < (w['top'] - x['top']) < 15 and 45 <= x['x0'] <= 95]
            d_cand.sort(key=lambda x: x['x0'])
            d_str = " ".join([x['text'] for x in d_cand])
            m = re.search(r'^(\d+)', d_str)
            day_num = int(m.group(1)) if m else 1
            tx_meta.append({
                'idx': len(tx_meta) + 1,
                'page': p_idx + 1,
                'day': day_num,
                'date_str': d_str,
                'time_str': time_str
            })

print(f"Total extracted tx: {len(tx_meta)}")
for t in tx_meta:
    print(f"Tx #{t['idx']:02d} (P{t['page']}): {t['date_str']} | {t['time_str']}")
