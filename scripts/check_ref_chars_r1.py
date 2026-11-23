import pdfplumber

ref_p = r'C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\.user_uploaded\media_1794538873844_ae928147.pdf'

with pdfplumber.open(ref_p) as pdf:
    p0 = pdf.pages[0]
    chars = p0.chars
    for c in chars:
        if c['top'] > 165 and c['top'] < 172 and c['x0'] > 295 and c['x0'] < 420:
            print(f"'{c['text']}' font={c['fontname']} size={c['size']:.1f} x0={c['x0']:.2f} x1={c['x1']:.2f}")
