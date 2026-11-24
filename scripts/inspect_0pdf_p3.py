import pdfplumber

with pdfplumber.open(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\aug\0.pdf') as pdf:
    p3 = pdf.pages[2]
    words = p3.extract_words()
    for w in sorted(words, key=lambda x: (x['top'], x['x0'])):
        if 350 <= w['top'] <= 750:
            print(f"{w['top']:.2f}, {w['x0']:.2f}-{w['x1']:.2f}: {w['text']}")
