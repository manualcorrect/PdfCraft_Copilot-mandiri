import pdfplumber

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\okt\0.pdf"
with pdfplumber.open(pdf_path) as pdf:
    p7 = pdf.pages[6]
    words = p7.extract_words()
    print("Page 7 top words (top < 150):")
    for w in sorted(words, key=lambda x: (x['top'], x['x0'])):
        if w['top'] < 150:
            print(f"  {w['text']} at top={w['top']:.2f}, x0={w['x0']:.2f}")
