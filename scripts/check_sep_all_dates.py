import pdfplumber

rev_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_sep byk harus revisi.pdf"

with pdfplumber.open(rev_path) as pdf:
    for p_idx, page in enumerate(pdf.pages, 1):
        words = page.extract_words()
        no_words = [w for w in words if abs(w['x0'] - 20.0) < 5 and 200 < w['top'] < 780 and w['text'].isdigit()]
        no_words.sort(key=lambda w: w['top'])
        for nw in no_words:
            no_val = int(nw['text'])
            y = nw['top']
            dt_words = [w for w in words if 45 <= w['x0'] < 118 and abs(w['top'] - y) < 14]
            dt_words.sort(key=lambda w: (round(w['top'], 1), w['x0']))
            print(f"Row {no_val:2d} (P{p_idx}): {' '.join(w['text'] for w in dt_words)}")
