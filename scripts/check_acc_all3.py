import pdfplumber

def check_acc(path, name):
    print(f"\n=== {name} ===")
    try:
        with pdfplumber.open(path) as pdf:
            words = pdf.pages[0].extract_words()
            for w in words:
                if any(k in w['text'] for k in ['1630', '1650', 'Nomor']):
                    print(f"{w['text']:<25} x0={w['x0']:.2f}, x1={w['x1']:.2f}, top={w['top']:.2f}")
    except Exception as e:
        print(f"Error {name}: {e}")

check_acc(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\REK_GALANG_AUG_2026_CHRONOLOGICAL.pdf", "AUG")
check_acc(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_SEP_2026_CHRONOLOGICAL.pdf", "SEP")
check_acc(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\REK_GALANG_OCT_2026_CHRONOLOGICAL.pdf", "OCT")
