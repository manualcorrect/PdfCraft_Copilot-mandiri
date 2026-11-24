import pdfplumber

ref_path = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\REK GAJI OKTOBER IBNU AGUN.pdf'
with pdfplumber.open(ref_path) as pdf:
    # Check page 6 and 7
    for p_num in [6, 7]:
        page = pdf.pages[p_num - 1]
        words = page.extract_words()
        print(f"=== IBNU AGUN OKT PAGE {p_num} ===")
        wibs = sorted([w for w in words if w['text'] == 'WIB' and w['top'] > 180], key=lambda x: x['top'])
        for w in wibs:
            y = w['top']
            r_words = [x for x in words if abs(x['top'] - y) < 15]
            r_words.sort(key=lambda x: x['x0'])
            print(f"  [Top {y:.1f}]: {' | '.join([x['text'] for x in r_words])}")
