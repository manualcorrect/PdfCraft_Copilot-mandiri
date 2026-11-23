import pdfplumber

with pdfplumber.open(r'output\temp_OCT_numbered_assembly.pdf') as pdf:
    for c in pdf.pages[0].chars:
        if 'Helvetica' in c.get('fontname', ''):
            print(f"temp_OCT has Helvetica: {c}")
