import pdfplumber

with pdfplumber.open(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\1.pdf') as pdf:
    for c in pdf.pages[0].chars:
        if 660 <= c['top'] <= 730 and 115 <= c['x0'] <= 350:
            print(f"{repr(c['text'])} | font={c['fontname']}")
