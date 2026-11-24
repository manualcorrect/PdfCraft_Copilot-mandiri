import pdfplumber

with pdfplumber.open(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\sep\0.pdf') as pdf:
    p5 = pdf.pages[4]
    words = p5.extract_words()
    for w in sorted(words, key=lambda x: (x['top'], x['x0'])):
        if w['top'] < 200:
            print(f"{w['top']:.2f}, {w['x0']:.2f}: {w['text']}")
