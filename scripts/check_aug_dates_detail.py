import pdfplumber

aug_edited = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\REK_GALANG_AUG_2026_edited ketengangan.pdf"

with pdfplumber.open(aug_edited) as pdf:
    tx_idx = 0
    for p_idx, page in enumerate(pdf.pages):
        words = page.extract_words()
        min_top = 320 if p_idx == 0 else 200
        table_words = [w for w in words if min_top <= w['top'] <= 800]
        wibs = sorted([w for w in table_words if w['text'] == 'WIB'], key=lambda x: x['top'])
        for w in wibs:
            tx_idx += 1
            date_words = [d['text'] for d in table_words if 0 < (w['top'] - d['top']) < 15 and 45 <= d['x0'] <= 95]
            time_words = [t['text'] for t in table_words if abs(t['top'] - w['top']) < 3 and t['x1'] <= w['x0'] + 1]
            date_str = " ".join(date_words)
            time_str = " ".join(time_words) + " WIB"
            print(f"Row {tx_idx:02d}: {date_str} | {time_str}")
