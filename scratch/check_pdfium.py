import pypdfium2 as pdfium

doc = pdfium.PdfDocument(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf")
print("PdfDocument methods:", [m for m in dir(doc) if not m.startswith('_')])
page = doc[0]
print("PdfPage methods:", [m for m in dir(page) if not m.startswith('_')])
doc.close()
