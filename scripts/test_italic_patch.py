import re
import zlib
import pypdfium2

PDF_IN = r"output\REK_KEISYA_AUG_OUTPUT_1.pdf"
PDF_OUT = r"output\test_italic6.pdf"

with open(PDF_IN, "rb") as f:
    pdf_bytes = f.read()

# 1. Parse XRef stream (Obj 553)
m_xref = re.search(rb'\b553\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
xref_dict = m_xref.group(1)
xref_stream = m_xref.group(2)
xref_decomp = zlib.decompress(xref_stream)

cols = 5
stride = cols + 1
rows = []
prev = bytearray(cols)
for i in range(554):
    row_bytes = xref_decomp[i*stride : (i+1)*stride]
    filter_type = row_bytes[0]
    curr = bytearray(row_bytes[1:])
    if filter_type == 2:
        for c in range(cols):
            curr[c] = (curr[c] + prev[c]) % 256
    prev = curr
    f1 = curr[0]
    f2 = (curr[1] << 8) | curr[2]
    f3 = (curr[3] << 8) | curr[4]
    rows.append([f1, f2, f3])

header_end = pdf_bytes.find(b"11 0 obj")
header = pdf_bytes[:header_end]

top_objs = [11, 112, 113, 213, 312, 411, 511, 532, 534, 536, 537, 538, 540, 542, 544, 545, 546, 547, 548, 549, 550, 551, 552]
obj_raw = {}
for i in range(len(top_objs)):
    oid = top_objs[i]
    m_start = re.search(rb'\b' + str(oid).encode() + rb'\s+0\s+obj\b', pdf_bytes)
    start_idx = m_start.start()
    if i + 1 < len(top_objs):
        next_oid = top_objs[i+1]
        end_idx = re.search(rb'\b' + str(next_oid).encode() + rb'\s+0\s+obj\b', pdf_bytes).start()
    else:
        end_idx = m_xref.start()
    obj_raw[oid] = pdf_bytes[start_idx:end_idx]

# Map page objects: Page 1 is Obj 11, Page 2 is Obj 113, Page 3 is Obj 213, Page 4 is Obj 312, Page 5 is Obj 411
page_objs = [11, 113, 213, 312, 411]

for p_num, oid in enumerate(page_objs, 1):
    raw = obj_raw[oid]
    m_stream = re.search(rb'stream[\r\n]+(.*?)[\r\n]+endstream', raw, re.DOTALL)
    stream_data = m_stream.group(1)
    decomp = zlib.decompress(stream_data)
    
    # Old block:
    # <003{p_num}0020006F006600200036> Tj
    p_hex = f"{(0x30 + p_num):02X}" # e.g. 31, 32...
    old_target = f"<00{p_hex}0020006F006600200036> Tj".encode()
    
    # Exact x offset from cm origin so that '6' starts at exactly 555.77 pt:
    page_offsets = {
        1: 555.77 - 542.40,
        2: 555.77 - 540.56,
        3: 555.77 - 540.52,
        4: 555.77 - 540.64,
        5: 555.77 - 540.44
    }
    w_prefix = page_offsets[p_num]
    new_replacement = f"<00{p_hex}0020006F00660020> Tj\n/R1 8 Tf\n1 0 0.2 1 {w_prefix:.2f} 0 Tm\n<0036> Tj".encode()
    
    if old_target in decomp:
        decomp = decomp.replace(old_target, new_replacement, 1)
        print(f"Replaced page {p_num} in Obj {oid}")
    else:
        print(f"Old target {old_target} not found in Obj {oid}")
        
    new_comp = zlib.compress(decomp, 9)
    before_stream = raw[:m_stream.start()]
    new_before_stream = re.sub(rb'/Length\s+\d+', f'/Length {len(new_comp)}'.encode(), before_stream)
    after_stream = raw[m_stream.end():]
    obj_raw[oid] = new_before_stream + b"stream\n" + new_comp + b"\nendstream" + after_stream

# Reassemble
out = bytearray(header)
for oid in top_objs:
    new_offset = len(out)
    rows[oid][1] = new_offset
    out.extend(obj_raw[oid])

xref_start = len(out)
rows[553][1] = xref_start

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
xref_obj_str = b'553 0 obj\n<<' + new_xref_dict + b'>>\nstream\n' + comp_xref + b'\nendstream\nendobj\nstartxref\n' + str(xref_start).encode() + b'\n%%EOF\n'
out.extend(xref_obj_str)

with open(PDF_OUT, "wb") as f:
    f.write(out)

print(f"Saved {PDF_OUT}")

# Render crop
doc = pypdfium2.PdfDocument(PDF_OUT)
im1 = doc[0].render(scale=2.0).to_pil()
w, h = im1.size
crop_hdr = im1.crop((int(0.85 * w), int(0.10 * h), w, int(0.18 * h)))
crop_hdr.save("output/test_italic6_crop.png")
print("Saved output/test_italic6_crop.png")
