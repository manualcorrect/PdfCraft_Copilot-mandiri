import pdfplumber

with pdfplumber.open(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\okt\0.pdf') as pdf:
    p4 = pdf.pages[3]
    words = p4.extract_words()
    wibs = sorted([w for w in words if w['text'] == 'WIB' and w['top'] > 180], key=lambda x: x['top'])
    for r_i, w in enumerate(wibs):
        y = w['top']
        r_words = [x for x in words if abs(x['top'] - y) < 15]
        r_words.sort(key=lambda x: x['x0'])
        row_line = " | ".join([f"{x['text']} (x0={x['x0']:.1f}, x1={x['x1']:.1f})" for x in r_words])
        print(f"Row {r_i+1:2d} (Tx {r_i+35:2d}) [Y={y:.1f}]: {row_line}")
