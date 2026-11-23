import re
import zlib
import io
import sys
from fontTools.ttLib import TTFont

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\okt\0.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

# Find all streams and decompress them
for m in re.finditer(rb'(\d+)\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL):
    oid = int(m.group(1))
    dict_part = m.group(2)
    stream_bytes = m.group(3)
    try:
        dec = zlib.decompress(stream_bytes)
        if b'/BaseFont' in dec:
            print(f"Obj {oid} has /BaseFont in decompressed data:")
            for line in dec.splitlines():
                if b'/BaseFont' in line:
                    print("  ", line[:100])
        if dec[:4] in [b'\x00\x01\x00\x00', b'OTTO', b'true']:
            ttf = TTFont(io.BytesIO(dec))
            name = ttf['name'].getDebugName(6) if 'name' in ttf else 'unknown'
            print(f"Obj {oid} is TTF: {name}, glyphs={len(ttf.getGlyphOrder())}")
        if b'/CIDInit' in dec:
            print(f"Obj {oid} is CMap / ToUnicode, len={len(dec)}")
    except Exception as e:
        pass
