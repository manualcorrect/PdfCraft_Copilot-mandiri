import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

galang_jul = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\REK GALANG JUL 2026.pdf"
galang_aug = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\REK GALANG AUG 2026.pdf"

print("=== GALANG JUL 2026 ORIGINAL NAME INSPECTION ===")
with pdfplumber.open(galang_jul) as pdf:
    for w in pdf.pages[0].extract_words():
        if w['top'] < 140 and any(k in w['text'] for k in ['GALANG', 'PUTRA', 'KURNIAWAN']):
            print(f"  {w['text']:20s} | x0={w['x0']:6.2f}, x1={w['x1']:6.2f}, top={w['top']:6.2f}, bottom={w['bottom']:6.2f}")

print("\n=== GALANG AUG 2026 ORIGINAL NAME INSPECTION ===")
with pdfplumber.open(galang_aug) as pdf:
    for w in pdf.pages[0].extract_words():
        if w['top'] < 140 and any(k in w['text'] for k in ['GALANG', 'PUTRA', 'KURNIAWAN']):
            print(f"  {w['text']:20s} | x0={w['x0']:6.2f}, x1={w['x1']:6.2f}, top={w['top']:6.2f}, bottom={w['bottom']:6.2f}")
