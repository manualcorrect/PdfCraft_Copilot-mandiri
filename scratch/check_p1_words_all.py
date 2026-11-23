import pdfplumber

with pdfplumber.open(r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output\REK_KEISYA_AUG_OUTPUT_1.pdf") as pdf:
    p1 = pdf.pages[0]
    words = p1.extract_words()
    near = [x for x in words if 335 <= x['top'] <= 355]
    print("Words on Page 1 y=335-355:")
    for w in sorted(near, key=lambda x: x['x0']):
        print(f"'{w['text']}' at x0={w['x0']:.1f}, x1={w['x1']:.1f}, top={w['top']:.1f}")
