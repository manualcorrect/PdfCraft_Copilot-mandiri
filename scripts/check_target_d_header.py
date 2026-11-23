import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
import pdfplumber

target_d = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\REK_GALANG_AUG_2026_STANDARDIZED.pdf"

with pdfplumber.open(target_d) as pdf:
    words = [w for w in pdf.pages[0].extract_words() if w['top'] < 140]
    for w in sorted(words, key=lambda x: (x['top'], x['x0'])):
        print(f"  top={w['top']:.1f}, x0={w['x0']:.1f}, text={repr(w['text'])}")
