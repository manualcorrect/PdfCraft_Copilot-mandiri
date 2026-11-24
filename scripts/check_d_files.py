import os, pdfplumber

def check_file(path):
    print(f"=== {path} ===")
    if not os.path.exists(path):
        print("Does not exist")
        return
    with pdfplumber.open(path) as pdf:
        p3 = pdf.pages[2]
        words = p3.extract_words()
        for w in sorted(words, key=lambda x: (x['top'], x['x0'])):
            if 250 <= w['top'] <= 300:
                print(f"{w['top']:.2f}, {w['x0']:.2f}-{w['x1']:.2f}: {w['text']}")

base = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\aug"
check_file(os.path.join(base, "REK_WAFIQ_AUG_OUTPUT_1.pdf"))
check_file(os.path.join(base, "REK_WAFIQ_AUG_OUTPUT_PERFECT.pdf"))
