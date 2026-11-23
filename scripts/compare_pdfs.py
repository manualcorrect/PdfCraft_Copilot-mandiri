import pdfplumber

for name, path in [
    ("1.pdf", r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\1.pdf"),
    ("2.pdf", r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\2.pdf"),
    ("3.pdf", r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\3.pdf"),
    ("4.pdf", r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\4.pdf"),
]:
    with pdfplumber.open(path) as pdf:
        total_wibs = sum(len([w for w in p.extract_words() if w['text'] == 'WIB']) for p in pdf.pages)
        print(f"{name:8s}: pages={len(pdf.pages)} | total_wibs={total_wibs}")
