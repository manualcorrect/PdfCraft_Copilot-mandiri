import pdfplumber

ref3_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\3.pdf"

with pdfplumber.open(ref3_path) as pdf:
    p4 = pdf.pages[3]
    # inspect chars of p4
    for c in p4.chars:
        if 220 < c['top'] < 240 and c['x0'] < 130:
            print(f"c='{c['text']}' x0={c['x0']:.2f} x1={c['x1']:.2f} top={c['top']:.2f}")
