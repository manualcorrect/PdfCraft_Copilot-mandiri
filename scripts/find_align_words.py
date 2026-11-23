import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

with pdfplumber.open('output/test_align_right.pdf') as pdf:
    for w in pdf.pages[0].extract_words():
        if any(k in w['text'] for k in ['354', '500']):
            print(w)
