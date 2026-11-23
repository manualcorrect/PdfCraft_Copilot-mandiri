from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage

fp = open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf", "rb")
parser = PDFParser(fp)
doc = PDFDocument(parser)

target = '679.988,81'.encode('utf-16-be')

for i, page in enumerate(PDFPage.create_pages(doc)):
    if i == 4: # Page 5
        for c in page.contents:
            data = c.get_data()
            idx = data.find(target)
            if idx != -1:
                chunk = data[max(0, idx-60):idx+len(target)+30]
                print("Found in Page 5 stream:", repr(chunk))
