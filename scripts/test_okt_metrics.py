import re
import zlib
import io
import sys
from fontTools.ttLib import TTFont

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\okt\0.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

def get_stream(oid):
    m = re.search(rb'\b' + str(oid).encode() + rb'\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
    return zlib.decompress(m.group(2))

ttf_reg = TTFont(io.BytesIO(get_stream(541)))
map_reg = get_stream(539)

ttf_bold = TTFont(io.BytesIO(get_stream(544)))
map_bold = get_stream(543)

hmtx_reg = ttf_reg['hmtx']
units_reg = ttf_reg['head'].unitsPerEm
hmtx_bold = ttf_bold['hmtx']
units_bold = ttf_bold['head'].unitsPerEm

def get_reg_width(s):
    w = 0.0
    for ch in s:
        cid = ord(ch)
        gid = (map_reg[cid*2] << 8) | map_reg[cid*2 + 1]
        adv = hmtx_reg[f"glyph{gid:05d}"][0]
        w += (adv / units_reg) * 8.0
    return w

def get_bold_width(s):
    w = 0.0
    for ch in s:
        cid = ord(ch)
        gid = (map_bold[cid*2] << 8) | map_bold[cid*2 + 1]
        adv = hmtx_bold[f"glyph{gid:05d}"][0]
        w += (adv / units_bold) * 8.0
    return w

print("Testing Page Numbers:")
PAGE_RIGHT_X = 563.80
for p in range(1, 7):
    sb = f"{p} dari 7"
    si = f"{p} of 7"
    wb = get_bold_width(sb)
    wi = get_reg_width(si)
    print(f"Page {p}: '{sb}' width={wb:.3f} -> x={PAGE_RIGHT_X - wb:.2f} | '{si}' width={wi:.3f} -> x={PAGE_RIGHT_X - wi:.2f}")

print("\nTesting some No and Saldo widths:")
for n in [1, 10, 50, 70]:
    print(f"No {n}: width={get_reg_width(str(n)):.3f}")

sal_test = "12.710.881,81"
print(f"Saldo {sal_test}: bold width={get_bold_width(sal_test):.3f}")
