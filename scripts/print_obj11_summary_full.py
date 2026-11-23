import zlib
import re

aug_out_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\REK_KEISYA_AUG_OUTPUT_1.pdf"

with open(aug_out_pdf, "rb") as f:
    b = f.read()

m = re.search(rb'\b11\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', b, re.DOTALL)
dec = zlib.decompress(m.group(2))

pos = dec.find(b"446.12 667 cm")
pos_end = dec.find(b"Tabungan NOW IDR")
if pos_end == -1: pos_end = dec.find(b"\x00T\x00a\x00b\x00u\x00n\x00g\x00a\x00n")

print("Existing summary box in Obj 11:")
print(dec[pos-50:pos_end].decode('latin1', errors='ignore'))
