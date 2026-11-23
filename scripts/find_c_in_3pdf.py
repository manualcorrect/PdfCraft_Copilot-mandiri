import pdfplumber

with pdfplumber.open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\3.pdf") as pdf:
    for p_idx, page in enumerate(pdf.pages):
        for c in page.chars:
            if c['text'] == 'c' and 'TTInterphases-' in c['fontname'] and 'Italic' not in c['fontname'] and 'Bold' not in c['fontname']:
                print(f"P{p_idx+1} c: font={c['fontname']} top={c['top']} x0={c['x0']}")
                words = [w['text'] for w in page.extract_words() if abs(w['top'] - c['top']) < 5 and abs(w['x0'] - c['x0']) < 100]
                print('  Near words:', words)
