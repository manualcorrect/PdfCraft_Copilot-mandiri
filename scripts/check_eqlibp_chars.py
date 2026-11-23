import pdfplumber

with pdfplumber.open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\1.pdf") as pdf:
    chars = set()
    for p in pdf.pages:
        for c in p.chars:
            if c['fontname'] == 'EQLIBP+PDF-PDF-TTInterphases-':
                chars.add(c['text'])
    print("Exact chars in EQLIBP+PDF-PDF-TTInterphases-:")
    print(repr(''.join(sorted(chars))))
