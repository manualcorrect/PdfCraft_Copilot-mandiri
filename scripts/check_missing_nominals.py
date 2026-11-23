import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

with pdfplumber.open("output/REK_GALANG_JUL_2026_STANDARDIZED.pdf") as pdf:
    print("=== Page 1 words around row 7 and 9 ===")
    for w in pdf.pages[0].extract_words():
        if (600 <= w['top'] <= 640 or 700 <= w['top'] <= 730):
            print(f"  {w['text']:20s} | x0={w['x0']:6.2f}, x1={w['x1']:6.2f}, top={w['top']:6.2f}")
            
    print("\n=== Page 2 words around row 13, 15, 18 ===")
    for w in pdf.pages[1].extract_words():
        if (300 <= w['top'] <= 340 or 390 <= w['top'] <= 430 or 530 <= w['top'] <= 570):
            print(f"  {w['text']:20s} | x0={w['x0']:6.2f}, x1={w['x1']:6.2f}, top={w['top']:6.2f}")
