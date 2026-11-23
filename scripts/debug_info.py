import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

with pdfplumber.open(r"D:\X_Files\rekening\Reference\Roy\ilovepdf_unlocked\Agu 2026_unlocked.pdf") as pdf:
    p1 = pdf.pages[0]
    print("--- Customer Name and Branch in Agu 2026 (Ground Truth) ---")
    for c in p1.chars:
        if c["top"] < 140 and 115 < c["x0"] < 250:
            print(f"{repr(c['text']):5s} x0={c['x0']:.1f} top={c['top']:.1f} font={c['fontname']}")
