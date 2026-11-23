import pdfplumber

with pdfplumber.open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\0.pdf") as pdf:
    for p_idx in range(len(pdf.pages)):
        p = pdf.pages[p_idx]
        p_chars = [c for c in p.chars if c['top'] < 125 and c['x0'] > 500]
        if p_chars:
            last_c = sorted(p_chars, key=lambda x: x['x1'])[-1]
            print(f"Page {p_idx+1}: page num last char '{last_c['text']}' x1 = {last_c['x1']:.2f}")
