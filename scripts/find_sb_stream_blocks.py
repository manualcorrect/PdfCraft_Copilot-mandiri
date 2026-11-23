from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
import re

def find_summary_in_stream(pdf_path, name):
    print(f"\n================ {name} ================")
    with open(pdf_path, 'rb') as fp:
        parser = PDFParser(fp)
        doc = PDFDocument(parser)
        for page in PDFPage.create_pages(doc):
            contents = page.contents[0].get_data()
            stext = contents.decode('latin1', errors='ignore')
            
            # search for 298 667 or 0 -23.3 Td or Saldo Awal
            m = re.search(r'298\s+667\s+cm.*?(?=ET\s*Q)', stext, re.DOTALL)
            if m:
                print("Found '298 667 cm' block:")
                print(m.group(0))
            else:
                print("Could not find '298 667 cm' block!")
                # search for 'Saldo'
                for match in re.finditer(r'BT[^\n]*?Saldo[\s\S]*?ET', stext):
                    print("Found Saldo BT block:", match.group(0)[:300])
            break

find_summary_in_stream('output/REK_KEISYA_AUG_OUTPUT_1.pdf', 'AUG')
find_summary_in_stream('output/REK_KEISYA_SEP_OUTPUT_1.pdf', 'SEP')
find_summary_in_stream('output/REK_KEISYA_OKT_OUTPUT_1.pdf', 'OKT')
