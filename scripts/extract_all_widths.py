import pdfplumber

with pdfplumber.open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\0.pdf") as pdf:
    reg_widths = {}
    bold_widths = {}
    it_widths = {}
    for page in pdf.pages:
        for c in page.chars:
            font = c.get('fontname', '')
            ch = c['text']
            if 'Bold' in font:
                bold_widths[ch] = c['width']
            elif 'Italic' in font:
                it_widths[ch] = c['width']
            else:
                reg_widths[ch] = c['width']

print("Regular char widths (8pt):", reg_widths)
print("\nBold char widths (8pt):", bold_widths)
print("\nItalic char widths (8pt):", it_widths)
