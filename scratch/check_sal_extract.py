import pdfplumber

with pdfplumber.open(r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output\REK_KEISYA_AUG_OUTPUT_1.pdf") as pdf:
    p1 = pdf.pages[0]
    words = p1.extract_words()
    wibs = sorted([w for w in words if w['text'] == 'WIB' and w['top'] >= 320], key=lambda x: x['top'])
    for idx, w in enumerate(wibs):
        # find all words with abs(top - w['top']) < 12
        near = [x for x in words if abs(x['top'] - w['top']) < 12]
        # find saldo
        sal_words = [x for x in near if x['x0'] >= 500]
        sal_txt = sal_words[0]['text'] if sal_words else "NOT_FOUND"
        print(f"Row {idx+1}: wib_top={w['top']:.1f} sal='{sal_txt}'")
