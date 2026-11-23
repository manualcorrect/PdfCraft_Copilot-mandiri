from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
import re

fp = open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf", "rb")
parser = PDFParser(fp)
doc = PDFDocument(parser)

for i, page in enumerate(PDFPage.create_pages(doc)):
    if i < 5:
        for c in page.contents:
            raw = c.get_data().decode('latin1', errors='ignore')
            bt_et = re.findall(r'BT\s+(.*?)\s+ET', raw, re.DOTALL)
            print(f"Page {i+1} has {len(bt_et)} BT...ET blocks")
            # print first 5 blocks
            for b_idx in range(min(5, len(bt_et))):
                print(f"  P{i+1} B{b_idx}: {repr(bt_et[b_idx][:100])}")
