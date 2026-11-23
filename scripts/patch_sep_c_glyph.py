import zlib
import re
from fontTools.ttLib import TTFont
import io
import pdfplumber

pdf_path = "output/REK_IBNU_SEP_OUTPUT_1.pdf"
aug_pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\0.pdf"

with open(aug_pdf_path, "rb") as f:
    b_aug = f.read()

with open(pdf_path, "rb") as f:
    b_sep = f.read()

# August font 601
m_aug = re.search(rb'\b601\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', b_aug, re.DOTALL)
ttf_aug = TTFont(io.BytesIO(zlib.decompress(m_aug.group(2))))

# In output/REK_IBNU_SEP_OUTPUT_1.pdf, let's find the TTF object for RMHACJ and CIDToGIDMap object
# Parse XRef stream
sx_matches = re.findall(rb'startxref[\r\n]+(\d+)', b_sep)
xref_offset = int(sx_matches[-1])

m_xref = re.search(rb'\b(\d+)\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', b_sep[xref_offset-50:], re.DOTALL)
xref_oid = int(m_xref.group(1))
xref_dict = m_xref.group(2)
xref_stream = m_xref.group(3)
xref_start_pos = re.search(rb'\b' + str(xref_oid).encode() + rb'\s+0\s+obj\b', b_sep).start()

m_size = re.search(r'/Size\s+(\d+)', xref_dict.decode('latin1'))
size = int(m_size.group(1))
m_w = re.search(r'/W\s*\[\s*(\d+)\s+(\d+)\s+(\d+)\s*\]', xref_dict.decode('latin1'))
w1, w2, w3 = int(m_w.group(1)), int(m_w.group(2)), int(m_w.group(3))
cols = w1 + w2 + w3
stride = cols + 1
decomp_xref = zlib.decompress(xref_stream)

rows = []
prev = bytearray(cols)
for i in range(size):
    row_bytes = decomp_xref[i*stride : (i+1)*stride]
    filter_type = row_bytes[0]
    curr = bytearray(row_bytes[1:])
    if filter_type == 2:
        for c in range(cols):
            curr[c] = (curr[c] + prev[c]) % 256
    prev = curr
    f1 = curr[0] if w1 == 1 else 0
    f2 = (curr[w1] << 8) | curr[w1+1] if w2 == 2 else curr[w1]
    f3 = (curr[w1+w2] << 8) | curr[w1+w2+1] if w3 == 2 else curr[w1+w2]
    rows.append([f1, f2, f3])

top_objs = [i for i in range(size) if rows[i][0] == 1 and i != xref_oid]
top_objs.sort(key=lambda oid: rows[oid][1])

header = b_sep[:rows[top_objs[0]][1]]
obj_raw = {}
for i, oid in enumerate(top_objs):
    start_idx = rows[oid][1]
    end_idx = rows[top_objs[i+1]][1] if i + 1 < len(top_objs) else xref_start_pos
    obj_raw[oid] = b_sep[start_idx:end_idx]

# Find TTF object and map object
ttf_oid = None
map_oid = None

for oid in top_objs:
    raw = obj_raw[oid]
    m_s = re.search(rb'stream[\r\n]+(.*?)[\r\n]+endstream', raw, re.DOTALL)
    if m_s:
        try:
            dec = zlib.decompress(m_s.group(1))
            if len(dec) == 131072:
                # This is CIDToGIDMap! Check if cid 67 is 24
                if ((dec[67*2] << 8) | dec[67*2+1]) == 24:
                    map_oid = oid
            elif dec[:4] in [b'\x00\x01\x00\x00', b'true', b'typ1', b'OTTO']:
                # Check if it has 73 glyphs
                ttf_test = TTFont(io.BytesIO(dec))
                if len(ttf_test.getGlyphOrder()) == 73:
                    ttf_oid = oid
        except:
            pass

print(f"Discovered TTF OID: {ttf_oid}, Map OID: {map_oid}")
assert ttf_oid is not None and map_oid is not None

# 1. Patch TTF
raw_ttf = obj_raw[ttf_oid]
m_sttf = re.search(rb'stream[\r\n]+(.*?)[\r\n]+endstream', raw_ttf, re.DOTALL)
dec_ttf = zlib.decompress(m_sttf.group(1))
ttf_sep = TTFont(io.BytesIO(dec_ttf))

g_aug_c = ttf_aug.getGlyphOrder()[50]
g_sep_c = ttf_sep.getGlyphOrder()[49]
ttf_sep['glyf'][g_sep_c] = ttf_aug['glyf'][g_aug_c]
ttf_sep['hmtx'][g_sep_c] = ttf_aug['hmtx'][g_aug_c]

out_buf = io.BytesIO()
ttf_sep.save(out_buf)
new_ttf_bytes = out_buf.getvalue()
comp_ttf = zlib.compress(new_ttf_bytes, 9)

before_ttf = raw_ttf[:m_sttf.start()]
new_before_ttf = re.sub(rb'/Length\s+\d+', f'/Length {len(comp_ttf)}'.encode(), before_ttf)
after_ttf = raw_ttf[m_sttf.end():]
obj_raw[ttf_oid] = new_before_ttf + b"stream\n" + comp_ttf + b"\nendstream" + after_ttf

# 2. Patch CIDToGIDMap
raw_map = obj_raw[map_oid]
m_smap = re.search(rb'stream[\r\n]+(.*?)[\r\n]+endstream', raw_map, re.DOTALL)
dec_map = bytearray(zlib.decompress(m_smap.group(1)))
cid_c = ord('c') # 99
dec_map[cid_c*2] = 0
dec_map[cid_c*2 + 1] = 49
comp_map = zlib.compress(bytes(dec_map), 9)

before_map = raw_map[:m_smap.start()]
new_before_map = re.sub(rb'/Length\s+\d+', f'/Length {len(comp_map)}'.encode(), before_map)
after_map = raw_map[m_smap.end():]
obj_raw[map_oid] = new_before_map + b"stream\n" + comp_map + b"\nendstream" + after_map

# 3. Reassemble
out = bytearray(header)
for oid in top_objs:
    new_offset = len(out)
    rows[oid][1] = new_offset
    out.extend(obj_raw[oid])

xref_start = len(out)
rows[xref_oid][1] = xref_start

new_xref_uncompressed = bytearray()
for r in rows:
    new_xref_uncompressed.append(0)
    new_xref_uncompressed.append(r[0])
    new_xref_uncompressed.append((r[1] >> 8) & 0xFF)
    new_xref_uncompressed.append(r[1] & 0xFF)
    new_xref_uncompressed.append((r[2] >> 8) & 0xFF)
    new_xref_uncompressed.append(r[2] & 0xFF)

comp_xref = zlib.compress(bytes(new_xref_uncompressed), 9)
new_xref_dict = re.sub(rb'/Length\s+\d+', f'/Length {len(comp_xref)}'.encode(), xref_dict)

xref_obj_str = (
    f"{xref_oid} 0 obj\n<<".encode() + new_xref_dict + b'>>\nstream\n' +
    comp_xref + b'\nendstream\nendobj\nstartxref\n' + str(xref_start).encode() + b'\n%%EOF\n'
)
out.extend(xref_obj_str)

with open(pdf_path, 'wb') as f:
    f.write(out)
print(f"Patched TTF and CIDToGIDMap in {pdf_path} ({len(out)} bytes)")

# 4. Re-render Page 1 header
brain_dir = r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098"
with pdfplumber.open(pdf_path) as pdf:
    p1 = pdf.pages[0]
    crop_hdr = p1.crop((15, 80, 580, 260))
    im_hdr = crop_hdr.to_image(resolution=200)
    im_hdr.save(f"{brain_dir}/ibnu_sep_p1_header_fixed_c.png")
    print(f"Saved: {brain_dir}/ibnu_sep_p1_header_fixed_c.png")
