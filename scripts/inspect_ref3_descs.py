import pdfplumber

ref3_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\3.pdf"

with pdfplumber.open(ref3_path) as pdf:
    for page_idx, page in enumerate(pdf.pages, 1):
        words = page.extract_words()
        no_words = [w for w in words if abs(w['x0'] - 20.0) < 5 and 200 < w['top'] < 780 and w['text'].isdigit()]
        no_words.sort(key=lambda w: w['top'])
        for nw in no_words:
            no_val = int(nw['text'])
            y = nw['top']
            ket_words = [w for w in words if 118 <= w['x0'] < 360 and abs(w['top'] - y) < 16]
            lines_dict = {}
            for kw in ket_words:
                lk = round(kw['top'] / 3.0) * 3
                lines_dict.setdefault(lk, []).append(kw)
            lines = []
            for lk in sorted(lines_dict.keys()):
                lines.append(" ".join(w['text'] for w in sorted(lines_dict[lk], key=lambda w: w['x0'])))
            print(f"Row {no_val:2d} (P{page_idx}) [y={y:.1f}]:")
            for l in lines:
                print(f"    {l}")
