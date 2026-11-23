import pdfplumber

aug_pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\0.pdf"

with pdfplumber.open(aug_pdf_path) as pdf:
    doc = pdf.doc
    p1 = pdf.pages[0]
    res = p1.page_obj.resources
    print("Aug Font dict:", res.get('Font'))
    for k, v in res.get('Font', {}).items():
        fobj = v.resolve()
        print(k, fobj.get('BaseFont'))
        for df in fobj.get('DescendantFonts', []):
            dfobj = df.resolve()
            print("  Descendant:", dfobj.get('BaseFont'), "W len:", len(dfobj.get('W', [])))
            w = dfobj.get('W', [])
            # check if 99 is in w
            print("  W:", w)
