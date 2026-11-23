import pdfplumber

with pdfplumber.open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\sep\0.pdf") as pdf:
    p8 = pdf.pages[7]
    for w in sorted(p8.extract_words(), key=lambda x: (x['top'], x['x0'])):
        print(f"top={w['top']:.2f} x0={w['x0']:.2f} text='{w['text']}'")
