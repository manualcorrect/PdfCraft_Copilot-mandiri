import zlib
import re
import io
from fontTools.ttLib import TTFont

aug_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf"

with open(aug_pdf, "rb") as f:
    b0 = f.read()

# Find font objects in August
# In August, what were the TTF font objects?
for m in re.finditer(rb'(\d+)\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', b0, re.DOTALL):
    oid = int(m.group(1))
    try:
        dec = zlib.decompress(m.group(3))
        if dec[:4] in [b'\x00\x01\x00\x00', b'OTTO', b'true']:
            ttf = TTFont(io.BytesIO(dec))
            name = ttf['name'].getDebugName(6) if 'name' in ttf else 'unknown'
            print(f"Obj {oid} is TTF: {name}")
    except:
        pass
