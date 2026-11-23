import pdfplumber

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\okt\0.pdf"

with pdfplumber.open(pdf_path) as pdf:
    p6 = pdf.pages[5]
    for c in p6.chars:
        if c['top'] < 130 and c['x0'] > 500:
            print(f"Char: '{c['text']}', font: {c.get('fontname')}, size: {c.get('size')}, matrix: {c.get('matrix')}")
