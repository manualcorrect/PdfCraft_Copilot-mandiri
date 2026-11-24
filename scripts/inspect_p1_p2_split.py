import pdfplumber

with pdfplumber.open(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\sep\0.pdf') as pdf:
    for p_num in [1, 2]:
        p = pdf.pages[p_num - 1]
        print(f"=== PAGE {p_num} ===")
        words = p.extract_words()
        for w in sorted(words, key=lambda x: (x['top'], x['x0'])):
            if p_num == 1 and w['top'] > 700:
                print(f"{w['top']:.2f}, {w['x0']:.2f}-{w['x1']:.2f}: {w['text']}")
            elif p_num == 2 and w['top'] < 300:
                print(f"{w['top']:.2f}, {w['x0']:.2f}-{w['x1']:.2f}: {w['text']}")
