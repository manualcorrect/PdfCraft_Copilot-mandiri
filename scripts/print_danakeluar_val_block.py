import zlib
import re

aug_out_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\REK_KEISYA_AUG_OUTPUT_1.pdf"

with open(aug_out_pdf, "rb") as f:
    b = f.read()

m = re.search(rb'\b11\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', b, re.DOTALL)
dec = zlib.decompress(m.group(2))

target = b"<002D002000310030002E003700340039002E003700380030002C00300030>"
pos = dec.find(target)
print("Block around Dana Keluar value in Obj 11:")
print(dec[pos-300:pos+200].decode('latin1', errors='ignore'))
