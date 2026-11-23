from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage

with open('output/REK_KEISYA_AUG_OUTPUT_1.pdf', 'rb') as fp:
    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    for page in PDFPage.create_pages(doc):
        res = page.attrs.get('Resources')
        print("Page Resources keys:", res.keys())
        fonts = res.get('Font')
        print("Font dict:", fonts)
        for fname, fref in fonts.items():
            fobj = doc.getobj(fref.objid)
            print(f"\nFont {fname} (obj {fref.objid}):")
            print("BaseFont:", fobj.get('BaseFont'))
            print("Subtype:", fobj.get('Subtype'))
            print("Encoding:", fobj.get('Encoding'))
            print("ToUnicode:", fobj.get('ToUnicode'))
            tu = fobj.get('ToUnicode')
            if tu:
                tu_obj = doc.getobj(tu.objid)
                tu_data = tu_obj.get_data().decode('latin1', errors='ignore')
                print("ToUnicode snippet:\n", tu_data[:300])
        break
