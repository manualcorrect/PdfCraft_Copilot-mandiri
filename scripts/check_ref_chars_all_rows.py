import pdfplumber

ref_p = r'C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\.user_uploaded\media_1794538873844_ae928147.pdf'

with pdfplumber.open(ref_p) as pdf:
    p0 = pdf.pages[0]
    chars = p0.chars
    for row_idx, (y_min, y_max, rname) in enumerate([(188, 195, 'Dana Masuk'), (211, 218, 'Dana Keluar'), (235, 242, 'Saldo Akhir')]):
        print(f"\n=== {rname} ===")
        row_chars = [c for c in chars if c['top'] > y_min and c['top'] < y_max and c['x0'] > 295 and c['x0'] < 440]
        for c in row_chars:
            if c['text'] in ['/', 'I', 'O', 'C']:
                print(f"'{c['text']}' font={c['fontname']} size={c['size']:.1f} x0={c['x0']:.2f} x1={c['x1']:.2f}")
