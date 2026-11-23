from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\0.pdf"

with open(pdf_path, 'rb') as fp:
    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    for p_idx, page in enumerate(PDFPage.create_pages(doc)):
        print(f"\n--- PAGE {p_idx+1} ---")
        contents = page.contents
        c_ids = [c.objid for c in contents] if contents else []
        print(f"Contents obj IDs: {c_ids}")
        res = page.attrs.get('Resources')
        fonts = res.get('Font') if res else {}
        print(f"Fonts: {list(fonts.keys())}")
        for fname, fref in fonts.items():
            fobj = doc.getobj(fref.objid)
            print(f"  {fname}: BaseFont={fobj.get('BaseFont')}")
        break
