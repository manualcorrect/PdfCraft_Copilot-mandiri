import pdfplumber

with pdfplumber.open('templates/master_page_1.pdf') as pdf:
    chars = set(c['text'] for c in pdf.pages[0].chars)
    print("& present in master_page_1:", "&" in chars)
