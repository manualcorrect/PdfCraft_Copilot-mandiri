import pdfplumber

with pdfplumber.open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\3.pdf") as pdf:
    fonts = {}
    for p in pdf.pages:
        for c in p.chars:
            fname = c['fontname']
            if fname not in fonts: fonts[fname] = set()
            fonts[fname].add(c['text'])
    for fname, chars in fonts.items():
        print(f"\nFont {fname}:")
        print(repr(''.join(sorted(chars))))
