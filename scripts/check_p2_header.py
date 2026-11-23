import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

with pdfplumber.open("output/REK_GALANG_JUL_2026_STANDARDIZED.pdf") as pdf:
    p2 = pdf.pages[1]
    words = p2.extract_words()
    print("=== Page 2 Header Words (top < 150) ===")
    for w in sorted([w for w in words if w['top'] < 150], key=lambda x: (round(x['top'], 1), x['x0'])):
        print(f"top={w['top']:5.1f} | x0={w['x0']:6.2f} x1={w['x1']:6.2f} | {w['text']}")
