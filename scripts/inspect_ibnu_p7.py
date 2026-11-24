import pdfplumber

with pdfplumber.open(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\REK GAJI AGUSTUS IBNU AGUN.pdf') as pdf:
    p7 = pdf.pages[6] # Page 7
    words = p7.extract_words()
    for w in sorted(words, key=lambda x: (x['top'], x['x0'])):
        if 300 <= w['top'] <= 460:
            print(f"{w['top']:.2f}, {w['x0']:.2f}-{w['x1']:.2f}: {w['text']}")
