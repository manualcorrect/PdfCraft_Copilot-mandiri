import zlib
import re
import io
from fontTools.ttLib import TTFont

aug_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf"

with open(aug_pdf, "rb") as f:
    b0 = f.read()

def get_stream(oid):
    m = re.search(rb'\b' + str(oid).encode() + rb'\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', b0, re.DOTALL)
    return zlib.decompress(m.group(2))

for oid in [437, 438, 440, 441, 443, 444]:
    s = get_stream(oid)
    print(f"Obj {oid} decomp len: {len(s)}")

ttf_reg = TTFont(io.BytesIO(get_stream(439)))
ttf_bold = TTFont(io.BytesIO(get_stream(442)))
ttf_it = TTFont(io.BytesIO(get_stream(445)))

map_reg = get_stream(437)
map_bold = get_stream(441)
map_it = get_stream(444)

hmtx_bold = ttf_bold['hmtx']
units_bold = ttf_bold['head'].unitsPerEm

def get_bold_width(s):
    w = 0.0
    for ch in s:
        cid = ord(ch)
        gid = (map_bold[cid*2] << 8) | map_bold[cid*2 + 1]
        adv = hmtx_bold[f"glyph{gid:05d}"][0]
        w += (adv / units_bold) * 8.0
    return w

# Values in August:
# Saldo Awal: 1.498.768,81
# Dana Masuk: + 11.950.000,00
# Dana Keluar: - 10.749.780,00
# Saldo Akhir: 2.698.988,81

v_sawal = "1.498.768,81"
v_dmasuk = "+ 11.950.000,00"
v_dkeluar = "- 10.749.780,00"
v_sakhir = "2.698.988,81"

for label, val in [("Saldo Awal", v_sawal), ("Dana Masuk", v_dmasuk), ("Dana Keluar", v_dkeluar), ("Saldo Akhir", v_sakhir)]:
    w = get_bold_width(val)
    x0 = 567.00 - w
    print(f"{label:<15}: val='{val}' width={w:.4f} -> x0={x0:.4f}, x1=567.00")
