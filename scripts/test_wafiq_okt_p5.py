import pdfplumber

pdf_path = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\okt\0.pdf'
with pdfplumber.open(pdf_path) as pdf:
    p5 = pdf.pages[4]
    print("Page 5 words:")
    for w in p5.extract_words():
        if w['top'] < 160:
            print(f"  {w['text']} at x0={w['x0']:.2f}, top={w['top']:.2f}")
