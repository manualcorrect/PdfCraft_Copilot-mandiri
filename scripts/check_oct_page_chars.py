import pdfplumber

with pdfplumber.open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\1.pdf") as pdf:
    for p_idx, page in enumerate(pdf.pages):
        for c in page.chars:
            if 520 <= c['x0'] <= 580 and 90 <= c['top'] <= 130:
                print(f"P{p_idx+1} char: {repr(c['text']):5s} font={c['fontname']} size={c['size']} x0={c['x0']:.1f} top={c['top']:.1f}")
