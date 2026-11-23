from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage

with open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf", "rb") as fp:
    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    for page in PDFPage.create_pages(doc):
        fonts = page.attrs.get('Resources').get('Font')
        for fname, fref in fonts.items():
            fobj = doc.getobj(fref.objid)
            df = fobj.get('DescendantFonts')
            if df:
                df_obj = doc.getobj(df[0].objid)
                w_array = df_obj.get('W')
                widths = {}
                i = 0
                while i < len(w_array):
                    c1 = w_array[i]
                    elem = w_array[i+1]
                    if isinstance(elem, list):
                        for idx, w in enumerate(elem):
                            widths[c1 + idx] = w
                        i += 2
                    else:
                        c2 = elem
                        w = w_array[i+2]
                        for c in range(c1, c2+1):
                            widths[c] = w
                        i += 3
                print(f"Font {fname}: ord('/')=47 in widths? {47 in widths}, width={widths.get(47)}")
                print(f"  All CIDs in {fname}: {sorted(widths.keys())}")
        break
