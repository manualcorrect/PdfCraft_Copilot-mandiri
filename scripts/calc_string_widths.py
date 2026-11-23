from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage

def get_font_widths():
    with open('output/REK_KEISYA_AUG_OUTPUT_1.pdf', 'rb') as fp:
        parser = PDFParser(fp)
        doc = PDFDocument(parser)
        for page in PDFPage.create_pages(doc):
            fonts = page.attrs.get('Resources').get('Font')
            for fname, fref in fonts.items():
                fobj = doc.getobj(fref.objid)
                # check descendant font widths
                df = fobj.get('DescendantFonts')
                if df:
                    cfont = doc.getobj(df[0].objid)
                    w_array = cfont.get('W')
                    # parse W array
                    # format: c1 [w1 w2 ...] or c_first c_last w
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
                    
                    def text_width(text):
                        total = 0
                        for ch in text:
                            cid = ord(ch)
                            w = widths.get(cid, 1000)
                            total += (w / 1000.0) * 8.0 # 8 pt
                        return total
                    
                    print(f"--- Widths for {fname} ({fobj.get('BaseFont')}) ---")
                    for s in ['1.498.768,81', '+ 11.950.000,00', '- 10.749.780,00', '2.698.988,81',
                              '+ 11.379.332,00', '- 7.227.500,00', '6.850.820,81',
                              '+ 14.306.611,00', '- 8.446.550,00', '12.710.881,81',
                              ':', 'Saldo Awal', ' / Initial Balance']:
                        print(f"  '{s}': width = {text_width(s):.3f} pt -> x0 = {567.0 - text_width(s):.2f}")
            break

get_font_widths()
