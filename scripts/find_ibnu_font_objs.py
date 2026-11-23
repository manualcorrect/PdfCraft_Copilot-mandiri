import pypdf
import re

reader = pypdf.PdfReader(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\0.pdf")
p1 = reader.pages[0]
fonts = p1['/Resources']['/Font']
for f_name, f_obj in fonts.items():
    f_deref = f_obj.get_object()
    base_font = f_deref.get('/BaseFont', '')
    desc = f_deref.get('/FontDescriptor', {}).get_object()
    ff2 = desc.get('/FontFile2', None)
    w_obj = f_deref.get('/Widths', None)
    to_uni = f_deref.get('/ToUnicode', None)
    print(f"Font {f_name}: BaseFont={base_font}")
    print(f"  FontFile2 ref: {desc.get('/FontFile2')}")
    print(f"  Widths ref: {f_deref.get('/Widths')}")
    print(f"  ToUnicode ref: {f_deref.get('/ToUnicode')}")
