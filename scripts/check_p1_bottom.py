import pdfplumber

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\okt\0.pdf"

with pdfplumber.open(pdf_path) as pdf:
    p1 = pdf.pages[0]
    words = p1.extract_words()
    # print all words below top 600
    bottom_words = [w for w in words if w['top'] > 600]
    bottom_words.sort(key=lambda w: (w['top'], w['x0']))
    for w in bottom_words:
        print(f"top={w['top']:.1f} x0={w['x0']:.1f} text={w['text']}")
