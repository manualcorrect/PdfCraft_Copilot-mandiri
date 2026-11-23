from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

with open('output/REK_KEISYA_AUG_OUTPUT_1.pdf', 'rb') as fp:
    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    for gid in [27, 28, 29, 35]:
        obj = doc.getobj(gid)
        print(f"ExtGState R{gid}:", obj)
