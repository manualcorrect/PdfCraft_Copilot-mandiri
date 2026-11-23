from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage

for label, p in [('AUG', 'output/REK_KEISYA_AUG_OUTPUT_1.pdf'), ('SEP', 'output/REK_KEISYA_SEP_OUTPUT_1.pdf'), ('OKT', 'output/REK_KEISYA_OKT_OUTPUT_1.pdf')]:
    with open(p, 'rb') as fp:
        parser = PDFParser(fp)
        doc = PDFDocument(parser)
        for page in PDFPage.create_pages(doc):
            print(f"{label} Page 1 Contents obj:", page.contents[0].objid)
            break
