from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
import re

fp = open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf", "rb")
parser = PDFParser(fp)
doc = PDFDocument(parser)

for i, page in enumerate(PDFPage.create_pages(doc)):
    if i == 2:
        for c in page.contents:
            raw = c.get_data().decode('latin1', errors='ignore')
            bt_et = re.findall(r'BT\s+(.*?)\s+ET', raw, re.DOTALL)
            for idx in range(70, len(bt_et)):
                print(f"=== Block {idx} ===")
                print(bt_et[idx])
