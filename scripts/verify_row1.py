import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

with pdfplumber.open(r"C:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output\test_save.pdf") as pdf:
    p = pdf.pages[0]
    words = p.extract_words()
    for w in words:
        if any(k in w["text"] for k in ["09:", "01 Aug", "WIB", "70.000"]):
            print(f"{w['text']:15s} | x0={w['x0']:.2f}, x1={w['x1']:.2f}, top={w['top']:.2f}")
