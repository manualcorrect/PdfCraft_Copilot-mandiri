import pdfplumber

def check_tx22(path, name):
    print(f"\n=== {name} ===")
    with pdfplumber.open(path) as pdf:
        p2 = pdf.pages[1]
        words = [w for w in p2.extract_words() if abs(w['top'] - 733.92) < 25 and 120 <= w['x0'] <= 365]
        lines = {}
        for w in sorted(words, key=lambda x: (x['top'], x['x0'])):
            lines.setdefault(round(w['top'], 1), []).append(w['text'])
        for top, ws in sorted(lines.items()):
            print(f"  top={top:5.1f}: {' '.join(ws)}")

check_tx22(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\REK_GALANG_OCT_2026_CHRONOLOGICAL.pdf", "OCT CHRONOLOGICAL")
check_tx22(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_SEP_2026_CHRONOLOGICAL.pdf", "SEP CHRONOLOGICAL")
