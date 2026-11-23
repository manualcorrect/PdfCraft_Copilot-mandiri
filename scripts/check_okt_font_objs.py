import re
import zlib

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\okt\0.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

for m in re.finditer(rb'(\d+)\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL):
    oid = int(m.group(1))
    d = m.group(2)
    if b"/ObjStm" in d:
        print(f"Obj {oid} is ObjStm")
        dec = zlib.decompress(m.group(3))
        for fm in re.finditer(rb'<<(?:(?!>>).)*?/BaseFont\s*/([^\s>]+).*?>>', dec, re.DOTALL):
            print(f"  BaseFont: {fm.group(1).decode()}")
        for fm in re.finditer(rb'<<(?:(?!>>).)*?/FontFile\d?\s+(\d+)\s+0\s+R.*?>>', dec, re.DOTALL):
            print(f"  FontFile: {fm.group(0).decode('latin1', 'ignore')}")
