import pdfplumber

ref3_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\3.pdf"

with pdfplumber.open(ref3_path) as pdf:
    p4 = pdf.pages[3]
    chars = [c for c in p4.chars if 220 < c['top'] < 240 and c['x0'] < 300]
    chars.sort(key=lambda c: c['x0'])
    print("P4 chars around y=228 in 3.pdf:")
    for c in chars:
        print(f"  '{c['text']}' at x0={c['x0']:.2f}, top={c['top']:.2f}, font={c['fontname']}")
