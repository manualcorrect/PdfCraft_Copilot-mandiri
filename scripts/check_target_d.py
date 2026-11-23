import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
import pdfplumber

target_d = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\REK_GALANG_AUG_2026_STANDARDIZED.pdf"

if os.path.exists(target_d):
    print("Reading D: target file...")
    with pdfplumber.open(target_d) as pdf:
        words = [w for w in pdf.pages[0].extract_words() if w['top'] < 400]
        for w in words:
            if w['top'] > 320:
                print(f"  top={w['top']:.1f}, x0={w['x0']:.1f}, text={repr(w['text'])}")
else:
    print("Target D: file does not exist!")
