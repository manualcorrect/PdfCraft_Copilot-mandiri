from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\0.pdf"

with open(pdf_path, 'rb') as fp:
    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    for p_idx, page in enumerate(PDFPage.create_pages(doc)):
        contents = page.contents
        c_ids = [c.objid for c in contents] if contents else []
        print(f"Page {p_idx+1}: Contents OIDs = {c_ids}")
