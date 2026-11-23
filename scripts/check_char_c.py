import pdfplumber

with pdfplumber.open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\sep\0.pdf") as pdf:
    for page in pdf.pages:
        for c in page.chars:
            if c['text'] == 'c':
                print(f"Page {page.page_number} found 'c': font={c.get('fontname')} size={c.get('size')}")
                break
