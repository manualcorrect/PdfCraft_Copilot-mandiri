import zlib
import re

aug_out_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\REK_KEISYA_AUG_OUTPUT_1.pdf"

with open(aug_out_pdf, "rb") as f:
    b = f.read()

for m in re.finditer(rb'stream[\r\n]+(.*?)[\r\n]+endstream', b, re.DOTALL):
    try:
        dec = zlib.decompress(m.group(1))
        if b"2.698" in dec or b"11.950" in dec or b"10.749" in dec:
            print("Found in plain ascii!")
        # check UTF-16
        for chunk in [b"\x001\x001\x00.\x009\x005", b"\x001\x000\x00.\x007\x004", b"\x002\x00.\x006\x009\x008"]:
            if chunk in dec:
                print(f"Found {chunk} in decomp stream!")
                pos = dec.find(chunk)
                print(dec[max(0, pos-200):min(len(dec), pos+200)])
    except:
        pass
