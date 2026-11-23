import pdfplumber

with pdfplumber.open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\0.pdf") as pdf:
    p1 = pdf.pages[0]
    chars = p1.chars
    # map char to width in R2
    char_widths = {}
    for c in chars:
        if 'Bold' in c.get('fontname', ''):
            char_widths[c['text']] = c['width']
            
print("Known char widths in R2:", char_widths)

def get_text_width(text):
    return sum(char_widths.get(ch, 5.0) for ch in text)

vals = [
    "2.564.938,81",
    "+ 8.853.000,00",
    "- 5.308.440,00",
    "6.109.498,81"
]

target_x1 = 567.00
for v in vals:
    w = get_text_width(v)
    x0 = target_x1 - w
    print(f"Value: '{v}' | Width: {w:.3f} | x0: {x0:.2f} | x1: {target_x1:.2f}")
