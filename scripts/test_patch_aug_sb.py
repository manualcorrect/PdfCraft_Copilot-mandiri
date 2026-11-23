import zlib
import re
import pdfplumber

def to_hex(text):
    return ''.join(f'{ord(c):04X}' for c in text)

with open('output/REK_KEISYA_AUG_OUTPUT_1.pdf', 'rb') as f:
    pdf_data = f.read()

# Find Obj 11
pat = re.compile(rb'(11\s+0\s+obj\s*<<.*?/Length\s+)(\d+)(.*?>>\s*stream\r?\n)(.*?)(\r?\nendstream)', re.DOTALL)
m = pat.search(pdf_data)
assert m, "Obj 11 not found!"

dict_prefix = m.group(1)
old_len = m.group(2)
dict_suffix = m.group(3)
raw_stream = m.group(4)
endstream = m.group(5)

stream_text = zlib.decompress(raw_stream).decode('latin1', errors='ignore')

# 1. Block 1 (Colons & Labels)
pos_c1 = stream_text.find('446.12 667 cm')
pos_c4 = stream_text.find('446.12 597 cm')
start_b1 = stream_text.rfind('q', 0, pos_c1)
end_b1 = stream_text.find('Q', pos_c4) + 1

# 2. Block 2 (Values)
pos_vals = stream_text.find('505.96 667 cm')
start_b2 = stream_text.rfind('q', 0, pos_vals)
pos_now = stream_text.find('16 676 cm')
end_b2 = stream_text.rfind('q', 0, pos_now)

print(f"B1: {start_b1} to {end_b1}")
print(f"B2: {start_b2} to {end_b2}")

new_b1 = f"""q 1 0 0 1 0 0 cm
BT
1 0 0 1 446.12 667 Tm
/R1 8 Tf
0.38039 0.35294 0.35294 rg
<{to_hex(':')}> Tj
0 g
ET
BT
1 0 0 1 298 667 Tm
/R2 8 Tf
0.10196 0.10196 0.10196 rg
<{to_hex('Saldo Awal')}> Tj
0 g
/R3 8 Tf
0.10196 0.10196 0.10196 rg
<{to_hex('/Initial Balance')}> Tj
0 g
ET
BT
1 0 0 1 298 644 Tm
/R2 8 Tf
0.10196 0.10196 0.10196 rg
<{to_hex('Dana Masuk')}> Tj
0 g
/R3 8 Tf
0.10196 0.10196 0.10196 rg
<{to_hex('/Incoming Transactions')}> Tj
0 g
ET
BT
1 0 0 1 446.12 644 Tm
/R1 8 Tf
0.02353 0.66667 0.43529 rg
<{to_hex(':')}> Tj
0 g
ET
BT
1 0 0 1 298 621 Tm
/R2 8 Tf
0.10196 0.10196 0.10196 rg
<{to_hex('Dana Keluar')}> Tj
0 g
/R3 8 Tf
0.10196 0.10196 0.10196 rg
<{to_hex('/Outgoing Transactions')}> Tj
0 g
ET
BT
1 0 0 1 446.12 621 Tm
/R1 8 Tf
0.10196 0.10196 0.10196 rg
<{to_hex(':')}> Tj
0 g
ET
BT
1 0 0 1 298 597 Tm
/R2 8 Tf
0.10196 0.10196 0.10196 rg
<{to_hex('Saldo Akhir')}> Tj
0 g
/R3 8 Tf
0.10196 0.10196 0.10196 rg
<{to_hex('/Closing Balance')}> Tj
0 g
ET
BT
1 0 0 1 446.12 597 Tm
/R1 8 Tf
0.38039 0.35294 0.35294 rg
<{to_hex(':')}> Tj
0 g
ET
Q"""

new_b2 = f"""q 1 0 0 1 0 0 cm
BT
1 0 0 1 521.32 667 Tm
/R2 8 Tf
0.38039 0.35294 0.35294 rg
<{to_hex('1.498.768,81')}> Tj
0 g
ET
BT
1 0 0 1 506.58 644 Tm
/R2 8 Tf
0.02353 0.66667 0.43529 rg
<{to_hex('+ 11.950.000,00')}> Tj
0 g
ET
BT
1 0 0 1 508.13 621 Tm
/R2 8 Tf
0.10196 0.10196 0.10196 rg
<{to_hex('- 10.749.780,00')}> Tj
0 g
ET
BT
1 0 0 1 519.08 597 Tm
/R2 8 Tf
0.07451 0.29412 0.72941 rg
<{to_hex('2.698.988,81')}> Tj
0 g
ET
Q """

# Replace b2 first (higher offset) then b1
new_stream_text = stream_text[:start_b2] + new_b2 + stream_text[end_b2:]
new_stream_text = new_stream_text[:start_b1] + new_b1 + new_stream_text[end_b1:]

new_raw = zlib.compress(new_stream_text.encode('latin1'))

# Rebuild PDF
# We can rewrite the object with new length, and rebuild xref table
obj_header = dict_prefix + str(len(new_raw)).encode() + dict_suffix + b'stream\r\n'
new_obj = obj_header + new_raw + b'\r\nendstream'

# Reconstruct the whole file and fix XRef
# Simple way: rewrite file, recompute xref offsets
# Let's write a robust XRef rebuilder
parts = [
    pdf_data[:m.start()],
    new_obj,
    pdf_data[m.end():]
]
rebuilt = b''.join(parts)

# Fix xref table:
# Find startxref
sx_m = re.search(rb'startxref\r?\n(\d+)', rebuilt)
assert sx_m, "startxref not found"
old_xref_offset = int(sx_m.group(1))

# Find xref table
xref_m = re.search(rb'xref\r?\n(\d+)\s+(\d+)\r?\n', rebuilt)
assert xref_m, "xref header not found"
start_obj = int(xref_m.group(1))
num_objs = int(xref_m.group(2))

# Find all object positions
obj_positions = {}
for match in re.finditer(rb'(\d+)\s+0\s+obj', rebuilt):
    oid = int(match.group(1))
    obj_positions[oid] = match.start()

# Build new xref table
new_xref = f"xref\r\n0 {num_objs}\r\n".encode()
new_xref += b"0000000000 65535 f\r\n"
for oid in range(1, num_objs):
    pos = obj_positions.get(oid, 0)
    new_xref += f"{pos:010d} 00000 n\r\n".encode()

# Trailer
trailer_m = re.search(rb'trailer\s*<<.*?>>', rebuilt, re.DOTALL)
assert trailer_m, "trailer not found"
trailer = trailer_m.group(0)

new_pdf = rebuilt[:xref_m.start()] + new_xref + trailer + b"\r\nstartxref\r\n" + str(xref_m.start()).encode() + b"\r\n%%EOF\r\n"

with open('output/test_aug_perfect_sb.pdf', 'wb') as f:
    f.write(new_pdf)

print("Saved output/test_aug_perfect_sb.pdf")

# Inspect with pdfplumber
print("\n--- EXTRACTED WORDS WITH PDFPLUMBER ---")
with pdfplumber.open('output/test_aug_perfect_sb.pdf') as pdf:
    p0 = pdf.pages[0]
    words = p0.extract_words()
    sb_words = [w for w in words if w['x0'] > 250 and w['top'] < 260 and w['top'] > 150]
    sb_words.sort(key=lambda w: (round(w['top'], 1), w['x0']))
    for w in sb_words:
        print(f"{w['text']:<35} top={w['top']:<8.4f} bottom={w['bottom']:<8.4f} x0={w['x0']:<8.2f} x1={w['x1']:<8.2f}")
