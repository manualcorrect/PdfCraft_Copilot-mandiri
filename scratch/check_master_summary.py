import pdfplumber

with pdfplumber.open('templates/master_page_1.pdf') as pdf:
    p1 = pdf.pages[0]
    words = [w for w in p1.extract_words() if w['x0'] > 450 and 130 <= w['top'] <= 250]
    for w in sorted(words, key=lambda x: x['top']):
        print(f"master_page_1 summary: text={w['text']}, top={w['top']:.2f}, bottom={w['bottom']:.2f}, x0={w['x0']:.2f}")
