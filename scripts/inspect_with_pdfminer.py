from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
import zlib
import re

def inspect_page1(pdf_path, name):
    print(f"\n================ {name} ================")
    with open(pdf_path, 'rb') as fp:
        parser = PDFParser(fp)
        doc = PDFDocument(parser)
        for page in PDFPage.create_pages(doc):
            pdict = page.attrs
            print("Page resources:", pdict.get('Resources'))
            contents = page.contents
            print("Contents obj:", contents)
            if contents:
                c0 = contents[0].get_data()
                stext = c0.decode('latin1', errors='ignore')
                print("Stream length:", len(stext))
                fonts_used = set(re.findall(r'(/F\w+|/R\w+)\s+\d+(?:\.\d+)?\s+Tf', stext))
                print("Fonts used:", fonts_used)
                
                # Check for Dana Keluar
                print("\nLines mentioning Dana Keluar or 621 or 620:")
                for line in stext.split('\n'):
                    if any(k in line for k in ['Dana Keluar', 'Keluar', '621', '620', 'Outgoing']):
                        print(line)
            break

inspect_page1('output/REK_KEISYA_AUG_OUTPUT_1.pdf', 'AUG')
inspect_page1('output/REK_KEISYA_SEP_OUTPUT_1.pdf', 'SEP')
inspect_page1('output/REK_KEISYA_OKT_OUTPUT_1.pdf', 'OKT')
