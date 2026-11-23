import pdfplumber

with pdfplumber.open(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf') as pdf:
    p1 = pdf.pages[0]
    words = p1.extract_words()
    w_342 = [w for w in words if 335 <= w['top'] <= 355]
    print("Words around y=335-355 on Page 1:")
    for w in sorted(w_342, key=lambda x: x['x0']):
        print(f"  '{w['text']}' at x0={w['x0']:.1f}, x1={w['x1']:.1f}, top={w['top']:.1f}, bottom={w['bottom']:.1f}")
