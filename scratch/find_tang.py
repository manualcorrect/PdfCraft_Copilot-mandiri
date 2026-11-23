import os, pdfplumber, glob

for p in glob.glob(r'templates\*.pdf') + glob.glob(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\*.pdf'):
    try:
        with pdfplumber.open(p) as pdf:
            for p_idx, page in enumerate(pdf.pages):
                for c in page.chars:
                    if 'TANGERANG' in c.get('text', '') or 'Helvetica' in c.get('fontname', ''):
                        print(f"{p} (P{p_idx+1}) has Helvetica/TANGERANG: {c.get('fontname')}")
                        break
    except:
        pass
