import re
import zlib
import io
import sys
from fontTools.ttLib import TTFont

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\okt\0.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

# Let's inspect objects 535..560
for oid in range(535, 560):
    m = re.search(rb'\b' + str(oid).encode() + rb'\s+0\s+obj\s*<<(.*?)>>(?:\s*stream[\r\n]+(.*?)[\r\n]+endstream)?', pdf_bytes, re.DOTALL)
    if m:
        dict_part = m.group(1).decode('latin1', errors='ignore')
        has_stream = "stream" if m.group(2) else "no stream"
        # only print if interesting
        if any(k in dict_part for k in ['Font', 'Type', 'Subtype']):
            cleaned = " ".join(dict_part.split())[:100]
            print(f"Obj {oid}: {cleaned} ({has_stream})")
            if m.group(2):
                try:
                    dec = zlib.decompress(m.group(2))
                    if dec[:4] in [b'\x00\x01\x00\x00', b'OTTO', b'true']:
                        ttf = TTFont(io.BytesIO(dec))
                        print(f"   -> Valid TTF! glyphs={len(ttf.getGlyphOrder())}")
                    elif b'/CIDInit' in dec:
                        print(f"   -> ToUnicode CMap stream, len={len(dec)}")
                except Exception as e:
                    pass
