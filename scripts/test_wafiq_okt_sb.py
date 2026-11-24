import pdfplumber

pdf_path = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\okt\0.pdf'
with pdfplumber.open(pdf_path) as pdf:
    p1 = pdf.pages[0]
    words = p1.extract_words()
    sb_words = [w for w in words if 290 <= w['x0'] <= 580 and 140 <= w['top'] <= 250]
    sb_words.sort(key=lambda x: (x['top'], x['x0']))
    print("Summary box words:")
    for w in sb_words:
        print(f"  {w['text']} at x0={w['x0']:.2f}, top={w['top']:.2f}")
