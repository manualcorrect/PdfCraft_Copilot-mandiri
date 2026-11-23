import zlib

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\sep\0.pdf"
with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

import re
m = re.search(rb'\b647\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
dec = zlib.decompress(m.group(2))
pos2 = dec.find(b"\x00T\x00a\x00m\x00a\x00n")
print(dec[pos2-150:pos2+250])
