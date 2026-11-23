import pdfplumber

pdf_path = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\REK_GALANG_OCT_OUTPUT_1.pdf'
with pdfplumber.open(pdf_path) as pdf:
    for c in pdf.pages[0].chars:
        if 660 <= c['top'] <= 700 and 115 <= c['x0'] <= 350:
            print(f"{repr(c['text'])} | font={c['fontname']} | size={c['size']}")
