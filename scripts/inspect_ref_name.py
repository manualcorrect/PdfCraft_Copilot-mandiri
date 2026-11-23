import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

nasih_path = r"D:\X_Files\rekening\Reference\nasih 2024 new unlocked\ilovepdf_unlocked\e-Statement_XXXXXXXXX9210_01 Des 2024-31 Des 2024_unlocked.pdf"
roy_path = r"D:\X_Files\rekening\Reference\Roy\ilovepdf_unlocked\Agu 2026_unlocked.pdf"

print("=== NASIH NAME ===")
with pdfplumber.open(nasih_path) as pdf:
    for w in pdf.pages[0].extract_words():
        if w['top'] < 140 and any(k in w['text'] for k in ['MUHAMMAD', 'NASIH']):
            print(f"  {w['text']:20s} | x0={w['x0']:6.2f}, x1={w['x1']:6.2f}, top={w['top']:6.2f}, bottom={w['bottom']:6.2f}")

print("\n=== ROY NAME ===")
with pdfplumber.open(roy_path) as pdf:
    for w in pdf.pages[0].extract_words():
        if w['top'] < 140 and any(k in w['text'] for k in ['ROY', 'DARWIN', 'REZERIUS']):
            print(f"  {w['text']:20s} | x0={w['x0']:6.2f}, x1={w['x1']:6.2f}, top={w['top']:6.2f}, bottom={w['bottom']:6.2f}")
