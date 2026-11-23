import pdfplumber

with pdfplumber.open(r"scratch/test_sal_align.pdf") as pdf:
    p3 = pdf.pages[2]
    words = p3.extract_words()
    near = [w for w in words if 725 <= w['top'] <= 750]
    for w in sorted(near, key=lambda x: x['x0']):
        print(f"'{w['text']}' at x0={w['x0']:.1f}, x1={w['x1']:.1f}, top={w['top']:.1f}")
