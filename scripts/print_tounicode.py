import re
import zlib

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\sep\0.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

for oid in [638, 640, 641, 643, 644, 646]:
    m = re.search(rb'\b' + str(oid).encode() + rb'\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
    if m:
        try:
            dec = zlib.decompress(m.group(2))
            if b"beginbfchar" in dec or b"beginbfrange" in dec:
                print(f"Obj {oid} is ToUnicode map:")
                print(dec.decode('latin1', 'ignore'))
        except:
            pass
