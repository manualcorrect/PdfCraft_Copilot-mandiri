import pdfplumber

print("=== 2.pdf Page 1 Characters in Keterangan (Row 1) ===")
with pdfplumber.open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\2.pdf") as pdf:
    chars = [c for c in pdf.pages[0].chars if 330 <= c['top'] <= 360 and 120 <= c['x0'] <= 250]
    fonts = set((c['fontname'], round(c['size'], 2)) for c in chars)
    print(f"Fonts in 2.pdf: {fonts}")
    # group by line top
    lines = {}
    for c in chars:
        lines.setdefault(round(c['top'], 1), []).append(c['text'])
    for top in sorted(lines.keys()):
        print(f"  top={top}: {''.join(lines[top])}")

print("\n=== REK_GALANG_AUG_2026_FINAL.pdf Page 1 Characters in Keterangan (Row 1) ===")
with pdfplumber.open(r"output\REK_GALANG_AUG_2026_STANDARDIZED.pdf") as pdf:
    chars = [c for c in pdf.pages[0].chars if 330 <= c['top'] <= 360 and 120 <= c['x0'] <= 250]
    fonts = set((c['fontname'], round(c['size'], 2)) for c in chars)
    print(f"Fonts in FINAL: {fonts}")
    lines = {}
    for c in chars:
        lines.setdefault(round(c['top'], 1), []).append(c['text'])
    for top in sorted(lines.keys()):
        print(f"  top={top}: {''.join(lines[top])}")
