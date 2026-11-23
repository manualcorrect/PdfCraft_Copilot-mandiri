import zlib, re
import pdfplumber

pdf_path = "output/REK_IBNU_SEP_OUTPUT_1.pdf"
with open(pdf_path, 'rb') as f:
    pdf_bytes = f.read()

sx_matches = re.findall(rb'startxref[\r\n]+(\d+)', pdf_bytes)
xref_offset = int(sx_matches[-1])

m_xref = re.search(rb'\b(\d+)\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes[xref_offset-50:], re.DOTALL)
xref_oid = int(m_xref.group(1))
xref_dict = m_xref.group(2)
xref_stream = m_xref.group(3)
xref_start_pos = re.search(rb'\b' + str(xref_oid).encode() + rb'\s+0\s+obj\b', pdf_bytes).start()

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

header = pdf_bytes[:rows[top_objs[0]][1]]
obj_raw = {}
for i, oid in enumerate(top_objs):
    start_idx = rows[oid][1]
    end_idx = rows[top_objs[i+1]][1] if i + 1 < len(top_objs) else xref_start_pos
    obj_raw[oid] = pdf_bytes[start_idx:end_idx]

# Modify ObjStm 752
raw752 = obj_raw[752]
m_s752 = re.search(rb'stream[\r\n]+(.*?)[\r\n]+endstream', raw752, re.DOTALL)
dict752 = raw752[:m_s752.start()]
dec752 = zlib.decompress(m_s752.group(1))

m_n = re.search(r'/N\s+(\d+)', dict752.decode('latin1'))
m_first = re.search(r'/First\s+(\d+)', dict752.decode('latin1'))
n = int(m_n.group(1))
first = int(m_first.group(1))

header_text = dec752[:first].decode('latin1')
nums = [int(x) for x in header_text.split()]
pairs = [(nums[i*2], nums[i*2+1]) for i in range(n)]

objs_data = []
for idx in range(n):
    start = first + pairs[idx][1]
    end = first + pairs[idx+1][1] if idx + 1 < n else len(dec752)
    chunk = dec752[start:end]
    if pairs[idx][0] == 729:
        print("Original 729:", chunk.decode('latin1'))
        chunk = chunk.replace(b'97 [520.019531 589.84375]', b'97 [520.019531 589.84375 535.15625]')
        print("Updated 729:", chunk.decode('latin1'))
    objs_data.append(chunk)

# Rebuild ObjStm 752
# Header format: pair of numbers. We can format with exact spacing or compute length iteratively
new_body = bytearray()
offsets = []
curr_off = 0
for chunk in objs_data:
    offsets.append(curr_off)
    new_body.extend(chunk)
    curr_off += len(chunk)

# format header string
# Let's ensure length convergence
hdr_tokens = []
for i in range(n):
    hdr_tokens.append(f"{pairs[i][0]} {offsets[i]}")
base_hdr = " ".join(hdr_tokens) + " \n"
new_first = len(base_hdr)

new_dec752 = base_hdr.encode('latin1') + new_body
comp752 = zlib.compress(new_dec752, 9)

new_dict752 = re.sub(r'/First\s+\d+', f'/First {new_first}', dict752.decode('latin1'))
new_dict752 = re.sub(r'/Length\s+\d+', f'/Length {len(comp752)}', new_dict752)
after752 = raw752[m_s752.end():]

obj_raw[752] = new_dict752.encode('latin1') + b"stream\n" + comp752 + b"\nendstream" + after752

# Reassemble
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
print("Updated ObjStm 752 in PDF!")

brain_dir = r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098"
with pdfplumber.open(pdf_path) as pdf:
    p1 = pdf.pages[0]
    crop_hdr = p1.crop((15, 80, 580, 260))
    im_hdr = crop_hdr.to_image(resolution=200)
    im_hdr.save(f"{brain_dir}/ibnu_sep_p1_header_fixed_c2.png")
    print(f"Saved: {brain_dir}/ibnu_sep_p1_header_fixed_c2.png")
