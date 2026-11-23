import pdfplumber

with pdfplumber.open(r'c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output\REK_KEISYA_AUG_OUTPUT_1.pdf') as pdf:
    p1 = pdf.pages[0]
    words = p1.extract_words()
    acc_words = [w for w in words if 180 <= w['top'] <= 210 and w['x0'] < 250]
    print("Words around y=180-210 on Page 1:")
    for w in acc_words:
        print(f"'{w['text']}' at x0={w['x0']:.1f}, top={w['top']:.1f}")
