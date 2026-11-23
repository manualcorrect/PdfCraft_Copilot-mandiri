import pdfplumber

def inspect_acc(path, name):
    print(f"=== {name} ===")
    try:
        with pdfplumber.open(path) as pdf:
            p0 = pdf.pages[0]
            words = p0.extract_words()
            for w in words:
                if any(k in w['text'] for k in ['Nomor', 'Account', 'Mata', 'Currency', '1630', '1650', '1660', 'IDR', ':']):
                    print(f"{w['text']:<35} x0={w['x0']:.2f}, x1={w['x1']:.2f}, top={w['top']:.2f}, bottom={w['bottom']:.2f}")
    except Exception as e:
        print(f"Error {name}: {e}")

inspect_acc(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\1.pdf", "ORIGINAL 1.pdf (OCT)")
inspect_acc(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\3.pdf", "ORIGINAL 3.pdf (SEP)")
inspect_acc(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\REK_GALANG_OCT_2026_CHRONOLOGICAL.pdf", "CURRENT OCT CHRONOLOGICAL")
inspect_acc(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_SEP_2026_CHRONOLOGICAL.pdf", "CURRENT SEP CHRONOLOGICAL")
