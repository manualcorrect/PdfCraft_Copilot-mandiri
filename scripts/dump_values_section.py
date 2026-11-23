from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage

with open('output/REK_KEISYA_AUG_OUTPUT_1.pdf', 'rb') as fp:
    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    for page in PDFPage.create_pages(doc):
        contents = page.contents[0].get_data()
        stext = contents.decode('latin1', errors='ignore')
        
        idx = stext.find('505.96 667 cm')
        if idx != -1:
            print("=== VALUES SECTION IN AUG ===")
            print(stext[idx:idx+2500])
        break
