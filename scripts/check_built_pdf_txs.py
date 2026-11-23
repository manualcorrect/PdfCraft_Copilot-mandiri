import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
import pdfplumber

with pdfplumber.open('output/REK_GALANG_AUG_2026_STANDARDIZED.pdf') as pdf:
    for p_idx, page in enumerate(pdf.pages):
        words = page.extract_words()
        print(f"=== Page {p_idx+1} Transactions ===")
        # extract date and time words
        dt_words = [w for w in words if 45 <= w['x0'] <= 110 and w['top'] > (320 if p_idx==0 else 200) and w['top'] < 800]
        # group by top
        lines = {}
        for w in dt_words:
            top_key = round(w['top'], 0)
            lines.setdefault(top_key, []).append(w['text'])
        for k in sorted(lines.keys()):
            print(f"  top~{k}: {' '.join(lines[k])}")
