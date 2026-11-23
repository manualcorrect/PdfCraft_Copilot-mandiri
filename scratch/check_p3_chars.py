import pdfplumber

with pdfplumber.open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf") as pdf:
    p3 = pdf.pages[2]
    chars = [c for c in p3.chars if 730 <= c['top'] <= 745 and (c['x0'] > 500 or c['x0'] < 40)]
    for c in sorted(chars, key=lambda x: x['x0']):
        print(f"'{c['text']}' at x0={c['x0']:.2f}, x1={c['x1']:.2f}, font={c.get('fontname')}")
