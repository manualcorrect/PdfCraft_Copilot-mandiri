import pdfplumber

with pdfplumber.open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\0.pdf") as pdf:
    p1 = pdf.pages[0]
    words = [w for w in p1.extract_words() if 290 <= w['x0'] <= 580 and 150 <= w['top'] <= 260]
    for w in sorted(words, key=lambda x: (x['top'], x['x0'])):
        print(f"{w['text']:<25} top={w['top']:.2f} x0={w['x0']:.2f} x1={w['x1']:.2f} width={w['x1']-w['x0']:.2f}")

    chars = [c for c in p1.chars if 500 <= c['x0'] <= 575 and 150 <= c['top'] <= 260]
    # Check widths of characters in R2
    r2_chars = [c for c in chars if 'Bold' in c.get('fontname', '')]
    print("\nSample character widths in R2:")
    seen_chars = set()
    for c in r2_chars:
        if c['text'] not in seen_chars:
            seen_chars.add(c['text'])
            print(f"'{c['text']}': width={c['width']:.3f}")
