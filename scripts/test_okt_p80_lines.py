import pdfplumber

pdf_path = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\okt\0.pdf'
with pdfplumber.open(pdf_path) as pdf:
    p3 = pdf.pages[2]
    words = p3.extract_words()
    p80_words = [w for w in words if 715 <= w['top'] <= 760 and 120 <= w['x0'] <= 300]
    p80_words.sort(key=lambda x: (x['top'], x['x0']))
    print("P80 words:")
    for w in p80_words:
        print(f"  {w['text']} at top={w['top']:.2f}, bottom={w['bottom']:.2f}, x0={w['x0']:.2f}")
