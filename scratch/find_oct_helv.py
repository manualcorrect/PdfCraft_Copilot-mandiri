import pdfplumber

pdf_path = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\REK_GALANG_OCT_OUTPUT_1.pdf'
with pdfplumber.open(pdf_path) as pdf:
    for p_idx, page in enumerate(pdf.pages):
        helv = [c for c in page.chars if 'Helvetica' in c.get('fontname', '')]
        if helv:
            txt = "".join([c['text'] for c in helv])
            print(f"Page {p_idx+1} has {len(helv)} Helvetica chars: {repr(txt[:60])}")
            for c in helv[:5]:
                print(f"  char={repr(c['text'])}, top={c['top']}, x0={c['x0']}")
