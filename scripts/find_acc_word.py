import pdfplumber

with pdfplumber.open("output/REK_IBNU_AUG_OUTPUT_1.pdf") as pdf:
    p1 = pdf.pages[0]
    words = p1.extract_words()
    for w in words:
        if '165' in w['text'] or '163' in w['text'] or 'Rekening' in w['text']:
            print(f"Match: '{w['text']}' top={w['top']:.2f} x0={w['x0']:.2f} x1={w['x1']:.2f}")
