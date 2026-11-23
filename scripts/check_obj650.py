import re
import zlib

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\sep\0.pdf"
with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

m = re.search(rb'\b650\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
if m:
    dec = zlib.decompress(m.group(2))
    pos = dec.find(b"RMHACJ")
    print("Context around RMHACJ:")
    print(dec[pos-100:pos+500].decode('latin1', 'ignore'))
