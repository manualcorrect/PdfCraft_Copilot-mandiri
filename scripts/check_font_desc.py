from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage

with open('output/test_aug_perfect_sb.pdf', 'rb') as fp:
    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    for page in PDFPage.create_pages(doc):
        fonts = page.attrs.get('Resources').get('Font')
        for fname, fref in fonts.items():
            fobj = doc.getobj(fref.objid)
            print(fname, fref.objid, fobj.get('FontDescriptor'))
            fd = fobj.get('FontDescriptor')
            if fd:
                fd_obj = doc.getobj(fd.objid)
                print("  FontBBox:", fd_obj.get('FontBBox'))
            df = fobj.get('DescendantFonts')
            if df:
                df_obj = doc.getobj(df[0].objid)
                dfd = df_obj.get('FontDescriptor')
                if dfd:
                    dfd_obj = doc.getobj(dfd.objid)
                    print("  Descendant FontBBox:", dfd_obj.get('FontBBox'))
        break
