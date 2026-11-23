import pdfplumber

with pdfplumber.open(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\REK_GALANG_OCT_2026_PERFECT.pdf') as pdf:
    for c in pdf.pages[0].chars:
        if 'TANGERANG' in c.get('text', '') or (670 <= c['top'] <= 725 and 120 <= c['x0'] <= 300):
            if c.get('fontname') != 'RRKPHJ+TTInterphases-Regular':
                print(f"Char: {repr(c['text'])}, font: {c.get('fontname')}")
