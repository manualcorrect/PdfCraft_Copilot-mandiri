import os
import sys
import pdfplumber

sys.stdout.reconfigure(encoding='utf-8')

mei_path = r"D:\X_Files\rekening\Reference\Roy\ilovepdf_unlocked\Mei 2026_unlocked.pdf"

with pdfplumber.open(mei_path) as pdf:
    print(f"Total pages in Mei 2026: {len(pdf.pages)}")
    last_page = pdf.pages[-1]
    print(f"=== Last Page (Page {len(pdf.pages)}) Words in Mei 2026 ===")
    for w in last_page.extract_words():
        print(f"  {w['text']:25s} | x0={w['x0']:6.2f}, x1={w['x1']:6.2f}, top={w['top']:6.2f}")
