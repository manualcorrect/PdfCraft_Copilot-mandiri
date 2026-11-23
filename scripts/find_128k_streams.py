import re
import zlib

okt_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\okt\0.pdf"
with open(okt_pdf, "rb") as f:
    b = f.read()

for m in re.finditer(rb'(\d+)\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', b, re.DOTALL):
    oid = int(m.group(1))
    try:
        dec = zlib.decompress(m.group(3))
        if len(dec) == 131072:
            print(f"Found 131072 stream at OID {oid}!")
    except:
        pass
