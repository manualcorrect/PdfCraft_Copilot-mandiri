from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
import re

with open('output/REK_KEISYA_AUG_OUTPUT_1.pdf', 'rb') as fp:
    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    for page in PDFPage.create_pages(doc):
        contents = page.contents[0].get_data()
        stext = contents.decode('latin1', errors='ignore')
        
        # Find where '298 667 cm' starts
        idx = stext.find('298 667 cm')
        if idx != -1:
            print("=== CONTEXT AROUND 298 667 cm in AUG ===")
            print(stext[idx-200:idx+2500])
        break
