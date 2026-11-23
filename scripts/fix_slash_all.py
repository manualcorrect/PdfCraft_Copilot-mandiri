import os
import re
import zlib
import pdfplumber
from PIL import Image

def to_hex(text):
    return ''.join(f'{ord(c):04X}' for c in text)

def patch_file(pdf_path, contents_oid):
    with open(pdf_path, 'rb') as f:
        pdf_bytes = f.read()

    # 1. Parse XRef stream
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
    decomp = zlib.decompress(xref_stream)
    
    rows = []
    prev = bytearray(cols)
    for i in range(size):
        row_bytes = decomp[i*stride : (i+1)*stride]
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

    # Extract header and objects
    header = pdf_bytes[:rows[top_objs[0]][1]]
    obj_raw = {}
    for i, oid in enumerate(top_objs):
        start_idx = rows[oid][1]
        if i + 1 < len(top_objs):
            next_oid = top_objs[i+1]
            end_idx = rows[next_oid][1]
        else:
            end_idx = xref_start_pos
        obj_raw[oid] = pdf_bytes[start_idx:end_idx]

    # Decompress Page 1 contents stream
    raw = obj_raw[contents_oid]
    m_stream = re.search(rb'stream[\r\n]+(.*?)[\r\n]+endstream', raw, re.DOTALL)
    stream_data = m_stream.group(1)
    stext = zlib.decompress(stream_data).decode('latin1', errors='ignore')

    # Find Block 1 (Colons & Labels)
    pos_c1 = stext.find('446.12 667')
    pos_b1_start = stext.rfind('q', 0, pos_c1)
    
    # End of Block 1 is after 446.12 597
    pos_c4 = stext.find('446.12 597')
    # Can be ET Q or ET\nQ
    m_end_b1 = re.search(r'ET\s*Q', stext[pos_c4:])
    assert m_end_b1, "End of B1 not found"
    pos_b1_end = pos_c4 + m_end_b1.end()

    # The clean Block 1 with '/' in /R2 (Bold)!
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
<{to_hex('Saldo Awal/')}> Tj
0 g
/R3 8 Tf
0.10196 0.10196 0.10196 rg
<{to_hex('Initial Balance')}> Tj
0 g
ET
BT
1 0 0 1 298 644 Tm
/R2 8 Tf
0.10196 0.10196 0.10196 rg
<{to_hex('Dana Masuk/')}> Tj
0 g
/R3 8 Tf
0.10196 0.10196 0.10196 rg
<{to_hex('Incoming Transactions')}> Tj
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
<{to_hex('Dana Keluar/')}> Tj
0 g
/R3 8 Tf
0.10196 0.10196 0.10196 rg
<{to_hex('Outgoing Transactions')}> Tj
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
<{to_hex('Saldo Akhir/')}> Tj
0 g
/R3 8 Tf
0.10196 0.10196 0.10196 rg
<{to_hex('Closing Balance')}> Tj
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

    new_stext = stext[:pos_b1_start] + new_b1 + stext[pos_b1_end:]

    new_comp = zlib.compress(new_stext.encode('latin1'), 9)
    before_stream = raw[:m_stream.start()]
    new_before_stream = re.sub(rb'/Length\s+\d+', f'/Length {len(new_comp)}'.encode(), before_stream)
    after_stream = raw[m_stream.end():]
    obj_raw[contents_oid] = new_before_stream + b"stream\n" + new_comp + b"\nendstream" + after_stream

    # Reassemble PDF and update XRef
    out = bytearray(header)
    for oid in top_objs:
        new_offset = len(out)
        rows[oid][1] = new_offset
        out.extend(obj_raw[oid])

    xref_start = len(out)
    rows[xref_oid][1] = xref_start

    new_xref_uncompressed = bytearray()
    for r in rows:
        new_xref_uncompressed.append(0) # Filter None
        new_xref_uncompressed.append(r[0])
        new_xref_uncompressed.append((r[1] >> 8) & 0xFF)
        new_xref_uncompressed.append(r[1] & 0xFF)
        new_xref_uncompressed.append((r[2] >> 8) & 0xFF)
        new_xref_uncompressed.append(r[2] & 0xFF)

    comp_xref = zlib.compress(bytes(new_xref_uncompressed), 9)
    new_xref_dict = re.sub(rb'/Length\s+\d+', f'/Length {len(comp_xref)}'.encode(), xref_dict)

    xref_obj_str = f"{xref_oid} 0 obj\n<<".encode() + new_xref_dict + b'>>\nstream\n' + comp_xref + b'\nendstream\nendobj\nstartxref\n' + str(xref_start).encode() + b'\n%%EOF\n'
    out.extend(xref_obj_str)

    with open(pdf_path, 'wb') as f:
        f.write(out)
    print(f"Patched and saved {pdf_path} ({len(out)} bytes)")

# Patch AUG, SEP, OKT
patch_file('output/REK_KEISYA_AUG_OUTPUT_1.pdf', 11)
patch_file('output/REK_KEISYA_SEP_OUTPUT_1.pdf', 10)
patch_file('output/REK_KEISYA_OKT_OUTPUT_1.pdf', 12)

# Verify with pdfplumber
print("\n--- VERIFY AUG EXTRACTED WORDS ---")
with pdfplumber.open('output/REK_KEISYA_AUG_OUTPUT_1.pdf') as pdf:
    p0 = pdf.pages[0]
    words = p0.extract_words()
    sb_words = [w for w in words if w['x0'] > 250 and w['top'] < 260 and w['top'] > 150]
    sb_words.sort(key=lambda w: (round(w['top'], 1), w['x0']))
    for w in sb_words:
        print(f"{w['text']:<35} top={w['top']:<8.4f} bottom={w['bottom']:<8.4f} x0={w['x0']:<8.2f} x1={w['x1']:<8.2f}")

# Render crop at 300 dpi
brain_dir = r'C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098'
crop_box = (280, 160, 580, 260)
with pdfplumber.open('output/REK_KEISYA_AUG_OUTPUT_1.pdf') as pdf:
    im = pdf.pages[0].crop(crop_box).to_image(resolution=300)
    im.save(f"{brain_dir}/sb_crop_aug_fixed_slash.png")
    print(f"Saved {brain_dir}/sb_crop_aug_fixed_slash.png")
