import pdfplumber

ref_2 = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\2.pdf"

with pdfplumber.open(ref_2) as pdf:
    all_chars = set()
    for p in pdf.pages:
        for c in p.chars:
            all_chars.add(c['text'])
            
print("Characters in 2.pdf:", sorted(list(all_chars)))
