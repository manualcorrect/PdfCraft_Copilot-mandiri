import pdfplumber

with pdfplumber.open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\1.pdf") as pdf:
    for p_idx, page in enumerate(pdf.pages):
        for c in page.chars:
            if c['text'] == 'c':
                print(f"P{p_idx+1} c: font={c['fontname']} adv={c.get('adv')}")
