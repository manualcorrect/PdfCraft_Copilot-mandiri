import pdfplumber

with pdfplumber.open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\sep\0.pdf") as pdf:
    p1 = pdf.pages[0]
    words = [w for w in p1.extract_words() if 280 <= w['x0'] <= 580 and 150 <= w['top'] <= 260]
    for w in sorted(words, key=lambda x: (x['top'], x['x0'])):
        print(f"{w['text']:<30} top={w['top']:.2f} x0={w['x0']:.2f} x1={w['x1']:.2f}")
