from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage

with open(r'C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\.user_uploaded\media_1794538873844_ae928147.pdf', 'rb') as fp:
    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    for page in PDFPage.create_pages(doc):
        fonts = page.attrs.get('Resources').get('Font')
        for fname, fref in fonts.items():
            fobj = doc.getobj(fref.objid)
            print(f"Ref Font {fname}: BaseFont={fobj.get('BaseFont')}")
            tu = fobj.get('ToUnicode')
            if tu:
                tu_obj = doc.getobj(tu.objid)
                data = tu_obj.get_data().decode('latin1', errors='ignore')
                print(f"ToUnicode for {fname}:\n{data[:400]}\n")
        break
