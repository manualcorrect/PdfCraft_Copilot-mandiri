import pdfplumber

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf"
with pdfplumber.open(pdf_path) as pdf:
    for p_idx, page in enumerate(pdf.pages):
        words = page.extract_words()
        wibs = sorted([w for w in words if w['text'] == 'WIB'], key=lambda x: x['top'])
        for idx, w in enumerate(wibs):
            t_candidates = [x for x in words if abs(x['top'] - w['top']) < 3 and x['x1'] <= w['x0'] + 1]
            time_str = f"{t_candidates[-1]['text']} WIB" if t_candidates else '12:00:00 WIB'
            d_candidates = [x for x in words if 0 < (w['top'] - x['top']) < 15 and 45 <= x['x0'] <= 95]
            d_candidates.sort(key=lambda x: x['x0'])
            d_str = " ".join([x['text'] for x in d_candidates])
            print(f"P{p_idx+1} Tx {idx+1:2d}: Date={d_str:<15} Time={time_str}")
