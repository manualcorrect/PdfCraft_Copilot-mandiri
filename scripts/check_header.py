import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

with pdfplumber.open(r"C:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output\REK_GALANG_AUG_2026_STANDARDIZED.pdf") as pdf:
    p1 = pdf.pages[0]
    words = p1.extract_words()
    print("=== All Words on Page 1 at top < 250 ===")
    for w in words:
        if w["top"] < 250:
            print(f"{w['text']:20s} | x0={w['x0']:.1f}, x1={w['x1']:.1f}, top={w['top']:.1f}")
