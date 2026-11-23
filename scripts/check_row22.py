import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
import pdfplumber

with pdfplumber.open('output/REK_GALANG_AUG_2026_STANDARDIZED.pdf') as pdf:
    p2 = pdf.pages[1]
    words = [w for w in p2.extract_words() if w['top'] > 720]
    for w in words:
        print(f"top={w['top']:.1f}, x0={w['x0']:.1f}, text={repr(w['text'])}")
