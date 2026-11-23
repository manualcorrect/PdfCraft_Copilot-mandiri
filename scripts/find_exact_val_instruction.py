import re
import zlib

aug_out_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\REK_KEISYA_AUG_OUTPUT_1.pdf"

with open(aug_out_pdf, "rb") as f:
    b = f.read()

# Find stream containing the summary box
for m in re.finditer(rb'stream[\r\n]+(.*?)[\r\n]+endstream', b, re.DOTALL):
    try:
        dec = zlib.decompress(m.group(1))
        if b"10.749" in dec or b"\x001\x000\x00.\x007\x004\x009" in dec:
            print("Found stream with 10.749.780,00:")
            # Find around 10.749
            pos = dec.find(b"10.749")
            if pos == -1: pos = dec.find(b"\x001\x000\x00.\x007\x004\x009")
            start = max(0, pos - 200)
            end = min(len(dec), pos + 200)
            print(dec[start:end])
    except:
        pass
