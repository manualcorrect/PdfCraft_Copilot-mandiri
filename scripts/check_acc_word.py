import pdfplumber

with pdfplumber.open("output/REK_IBNU_AUG_OUTPUT_1.pdf") as pdf:
    p1 = pdf.pages[0]
    words = [w for w in p1.extract_words() if 250 <= w['top'] <= 310]
    for w in sorted(words, key=lambda x: (x['top'], x['x0'])):
        print(f"Word: '{w['text']}' top={w['top']:.2f} x0={w['x0']:.2f} x1={w['x1']:.2f}")
