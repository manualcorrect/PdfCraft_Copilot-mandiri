import zlib
import re

aug_0_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf"

with open(aug_0_pdf, "rb") as f:
    b = f.read()

for m in re.finditer(rb'stream[\r\n]+(.*?)[\r\n]+endstream', b, re.DOTALL):
    try:
        dec = zlib.decompress(m.group(1))
        if b"Saldo Awal" in dec or b"\x00S\x00a\x00l\x00d\x00o\x00 \x00A\x00w\x00a" in dec:
            pos = dec.find(b"\x00S\x00a\x00l\x00d\x00o\x00 \x00A\x00w\x00a")
            print("Found labels in aug/0.pdf:")
            print(dec[max(0, pos-200):min(len(dec), pos+600)].decode('latin1', errors='ignore'))
    except:
        pass
