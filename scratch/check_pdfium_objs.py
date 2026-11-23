import pypdfium2 as pdfium

doc = pdfium.PdfDocument(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf")
p3 = doc[2]
for o in p3.get_objects():
    if o.type == 1:
        print("Methods on PdfTextObj:", [m for m in dir(o) if not m.startswith('_')])
        break
doc.close()
