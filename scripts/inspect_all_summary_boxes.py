import pdfplumber
import os

files = [
    ('AUG_LOCAL', 'output/REK_KEISYA_AUG_OUTPUT_1.pdf'),
    ('SEP_LOCAL', 'output/REK_KEISYA_SEP_OUTPUT_1.pdf'),
    ('OKT_LOCAL', 'output/REK_KEISYA_OKT_OUTPUT_1.pdf'),
    ('USER_REF', r'C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\.user_uploaded\media_1794538873844_ae928147.pdf')
]

for label, p in files:
    if not os.path.exists(p):
        print(f"File not found: {p}")
        continue
    print(f"\n==================== {label} ====================")
    with pdfplumber.open(p) as pdf:
        p0 = pdf.pages[0]
        words = p0.extract_words()
        sb_words = [w for w in words if w['x0'] > 250 and w['top'] < 260 and w['top'] > 150]
        sb_words.sort(key=lambda w: (round(w['top'], 1), w['x0']))
        for w in sb_words:
            print(f"{w['text']:<35} top={w['top']:<8.4f} bottom={w['bottom']:<8.4f} x0={w['x0']:<8.2f} x1={w['x1']:<8.2f}")
