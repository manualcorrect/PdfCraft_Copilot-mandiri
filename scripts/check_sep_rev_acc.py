import pdfplumber

sep_rev = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_sep byk harus revisi.pdf"

with pdfplumber.open(sep_rev) as pdf:
    p1 = pdf.pages[0]
    words = p1.extract_words()
    acc_words = [w for w in words if "1630016287487" in w['text'] or "165000" in w['text'] or "166000" in w['text']]
    for w in acc_words:
        print(f"Account number: '{w['text']}' at x0={w['x0']:.2f}, top={w['top']:.2f}")
        
    colon_words = [w for w in words if w['text'] == ':' and 160 < w['top'] < 200]
    for w in colon_words:
        print(f"Colon at x0={w['x0']:.2f}, top={w['top']:.2f}")
