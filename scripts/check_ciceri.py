import pdfplumber

def check(p):
    print("=== Checking:", p)
    with pdfplumber.open(p) as pdf:
        for c in pdf.pages[0].chars:
            if 45 <= c['x0'] <= 180 and abs(c['top'] - 125) < 15:
                print(f"{repr(c['text']):5s} font={c['fontname']} adv={c.get('adv')}")

check(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\REK_GALANG_AUG_2026_PERFECT.pdf")
check(r"output\REK_GALANG_SEP_2026_CHRONOLOGICAL.pdf")
