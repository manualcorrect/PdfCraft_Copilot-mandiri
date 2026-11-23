import pdfplumber

def check_header(path, name):
    print(f"\n=== {name} ===")
    with pdfplumber.open(path) as pdf:
        words = pdf.pages[0].extract_words()
        for w in words:
            if any(k in w['text'] for k in ['GALANG', 'ROY', 'DARWIN', 'KCP', 'Ciceri', 'Taman', 'Periode', 'Dicetak', '06 Nov', '09 Sep', '1630', '1650', 'IDR', 'Nomor', 'Mata']):
                print(f"{w['text']:<30} x0={w['x0']:.2f}, x1={w['x1']:.2f}, top={w['top']:.2f}")

check_header(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\1.pdf", "ORIGINAL 1.pdf")
check_header(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\REK_GALANG_OCT_2026_CHRONOLOGICAL.pdf", "OUTPUT OCT")
check_header(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_SEP_2026_CHRONOLOGICAL.pdf", "OUTPUT SEP")
