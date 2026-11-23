import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

with pdfplumber.open("output/REK_GALANG_JUL_2026_STANDARDIZED.pdf") as pdf:
    p1 = pdf.pages[0]
    words = p1.extract_words()
    print("=== Header words on Page 1 (top < 150) ===")
    for w in sorted([w for w in words if w['top'] < 150], key=lambda x: (round(x['top'], 1), x['x0'])):
        print(f"top={w['top']:5.1f} | x0={w['x0']:6.2f} x1={w['x1']:6.2f} | {w['text']}")
        
    print("\n=== Account & Currency (150 <= top < 230 and x0 < 250) ===")
    for w in sorted([w for w in words if 150 <= w['top'] < 230 and w['x0'] < 250], key=lambda x: (round(x['top'], 1), x['x0'])):
        print(f"top={w['top']:5.1f} | x0={w['x0']:6.2f} x1={w['x1']:6.2f} | {w['text']}")
        
    print("\n=== Summary Box (160 <= top < 260 and x0 > 290) ===")
    for w in sorted([w for w in words if 160 <= w['top'] < 260 and w['x0'] > 290], key=lambda x: (round(x['top'], 1), x['x0'])):
        print(f"top={w['top']:5.1f} | x0={w['x0']:6.2f} x1={w['x1']:6.2f} | {w['text']}")
