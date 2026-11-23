import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

with pdfplumber.open("output/REK_GALANG_JUL_2026_STANDARDIZED.pdf") as pdf:
    for w in pdf.pages[0].extract_words():
        if "16300" in w['text']:
            print(f"w: {w['text']} | x0={w['x0']}, x1={w['x1']}, top={w['top']}")
