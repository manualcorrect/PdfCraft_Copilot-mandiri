import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

with pdfplumber.open('templates/master_page_1.pdf') as pdf:
    p = pdf.pages[0]
    words = p.extract_words()
    print('Words in Y 90-130:')
    for w in sorted(words, key=lambda x: (x['top'], x['x0'])):
        if 90 <= w['top'] <= 130:
            print(f"  '{w['text']}' top={w['top']:.2f}, x0={w['x0']:.2f}, x1={w['x1']:.2f}")
