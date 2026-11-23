import pdfplumber

with pdfplumber.open('templates/master_page_1.pdf') as pdf:
    for c in pdf.pages[0].chars:
        if 660 <= c['top'] <= 700 and 115 <= c['x0'] <= 350:
            print(f"{repr(c['text'])} | font={c['fontname']}")
