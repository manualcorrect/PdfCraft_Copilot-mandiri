import zlib
import re

aug_0_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf"

with open(aug_0_pdf, "rb") as f:
    b = f.read()

# Find stream containing the summary box
for m in re.finditer(rb'stream[\r\n]+(.*?)[\r\n]+endstream', b, re.DOTALL):
    try:
        dec = zlib.decompress(m.group(1))
        if b"18.273" in dec or b"\x001\x008\x00.\x002\x007\x003" in dec:
            print("Found in aug 0.pdf:")
            pos = dec.find(b"18.273")
            if pos == -1: pos = dec.find(b"\x001\x008\x00.\x002\x007\x003")
            print(dec[max(0, pos-250):min(len(dec), pos+250)].decode('latin1', errors='ignore'))
    except:
        pass
