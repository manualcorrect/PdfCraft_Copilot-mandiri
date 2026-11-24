from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1

with open('output/test_sep_p3.pdf', 'rb') as fp:
    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    
    # Traverse pages
    def walk(obj):
        t = obj.get('Type')
        if t and t.name == 'Pages':
            for kid in resolve1(obj['Kids']):
                walk(resolve1(kid))
        elif t and t.name == 'Page':
            c = obj.get('Contents')
            print("Found Page:", obj)
            print("  Contents:", c)

    catalog = resolve1(doc.catalog)
    pages = resolve1(catalog['Pages'])
    walk(pages)
