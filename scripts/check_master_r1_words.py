import pdfplumber

with pdfplumber.open("templates/master_page_1.pdf") as pdf:
    p1 = pdf.pages[0]
    words = [w for w in p1.extract_words() if 330 <= w['top'] <= 365 and 120 <= w['x0'] <= 300]
    for w in sorted(words, key=lambda x: (x['top'], x['x0'])):
        print(f"top={w['top']:.2f}, x0={w['x0']:.2f}: {repr(w['text'])}")
