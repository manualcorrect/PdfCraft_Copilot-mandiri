"""
Patch and perfect REK_KEISYA_AUG_OUTPUT_1.pdf:
Updates all running balances (saldos) for rows 34 to 58 directly in the PDF streams,
preserving 100% of authentic Mandiri TTInterphases typography, geometry, and styling.
Regenerates the PDF XRef stream for complete PDF syntax integrity.
"""

import os
import re
import zlib
import openpyxl

PDF_PATH = r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output\REK_KEISYA_AUG_OUTPUT_1.pdf"
EXCEL_PATH = r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output\Template_Mutasi_AUG_OUTPUT_1.xlsx"

def to_utf16_be(s: str) -> bytes:
    return s.encode("utf-16-be")

def format_idr(num: float) -> str:
    return f"{abs(num):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def patch_keisya_saldos():
    print("=== PATCHING KEISYA AUGUST 2026 SALDOS ===")
    
    # 1. Read Excel running balances
    wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)
    ws = wb["Tabel_Mutasi"]
    excel_saldos = {}
    for idx in range(58):
        r = 6 + idx
        val = float(ws.cell(r, 7).value) + 0.81
        excel_saldos[idx + 1] = format_idr(val)
        
    print(f"Row 34 Saldo: {excel_saldos[34]}")
    print(f"Row 57 Saldo: {excel_saldos[57]}")
    print(f"Row 58 Saldo: {excel_saldos[58]}")

    with open(PDF_PATH, "rb") as f:
        pdf_bytes = f.read()

    # 2. Parse XRef stream (Obj 553)
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

    # 3. Extract header and objects 11 to 552
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

    # Helper to decompress and update an object stream
    def update_stream(oid, transform_fn):
        raw = obj_raw[oid]
        m_stream = re.search(rb'stream[\r\n]+(.*?)[\r\n]+endstream', raw, re.DOTALL)
        stream_data = m_stream.group(1)
        decomp = zlib.decompress(stream_data)
        
        new_decomp = transform_fn(decomp)
        new_comp = zlib.compress(new_decomp, 9)
        
        # update /Length in dict
        before_stream = raw[:m_stream.start()]
        new_before_stream = re.sub(rb'/Length\s+\d+', f'/Length {len(new_comp)}'.encode(), before_stream)
        after_stream = raw[m_stream.end():]
        
        new_raw = new_before_stream + b"stream\n" + new_comp + b"\nendstream" + after_stream
        obj_raw[oid] = new_raw

    # 4. Patch Obj 213 (Page 3 - Row 34 Saldo)
    def patch_213(decomp):
        old_utf = to_utf16_be("6.091.988,81")
        new_utf = to_utf16_be(excel_saldos[34])
        assert old_utf in decomp, "Old saldo for row 34 not found in Obj 213"
        return decomp.replace(old_utf, new_utf, 1)

    update_stream(213, patch_213)
    print("Patched Obj 213 (Row 34 Gaji)")

    # 5. Patch Obj 312 (Page 4 - Rows 35..46 Saldos)
    old_p4_saldos = [
        "6.060.988,81", "6.059.988,81", "6.009.988,81", "4.759.988,81", "4.509.988,81",
        "4.009.988,81", "4.007.988,81", "4.006.988,81", "3.956.988,81", "3.954.988,81",
        "3.952.488,81", "3.852.488,81"
    ]
    def patch_312(decomp):
        for r_idx, old_s in enumerate(old_p4_saldos):
            tx_no = 35 + r_idx
            old_utf = to_utf16_be(old_s)
            new_utf = to_utf16_be(excel_saldos[tx_no])
            assert old_utf in decomp, f"Old saldo {old_s} for row {tx_no} not found in Obj 312"
            decomp = decomp.replace(old_utf, new_utf, 1)
        return decomp

    update_stream(312, patch_312)
    print("Patched Obj 312 (Rows 35..46)")

    # 6. Patch Obj 411 (Page 5 - Rows 47..58 Saldos)
    old_p5_saldos = [
        "3.352.488,81", "3.351.488,81", "3.323.488,81", "3.322.488,81", "3.301.988,81",
        "3.801.988,81", "2.801.988,81", "1.801.988,81", "1.301.988,81", "1.001.988,81"
    ]
    def patch_411(decomp):
        # Rows 47..56 (same 12-char length)
        for r_idx, old_s in enumerate(old_p5_saldos):
            tx_no = 47 + r_idx
            old_utf = to_utf16_be(old_s)
            new_utf = to_utf16_be(excel_saldos[tx_no])
            assert old_utf in decomp, f"Old saldo {old_s} for row {tx_no} not found in Obj 411"
            decomp = decomp.replace(old_utf, new_utf, 1)
            
        # Row 57 (kerning adjustment for 10-char to 12-char)
        # Old: [ -62695(\x009\x007\x009\x00.\x009\x008\x008\x00,\x008\x001)]TJ
        # New: [ -61805(\x002\x00.\x007\x000\x003\x00.\x009\x008\x008\x00,\x008\x001)]TJ
        old_r57 = b"[ -62695(" + to_utf16_be("979.988,81") + b")]TJ"
        new_r57 = b"[ -61805(" + to_utf16_be(excel_saldos[57]) + b")]TJ"
        assert old_r57 in decomp, "Old pattern for Row 57 not found in Obj 411"
        decomp = decomp.replace(old_r57, new_r57, 1)

        # Row 58 (kerning adjustment for 10-char to 12-char)
        # Old: [ -62620(\x006\x007\x009\x00.\x009\x008\x008\x00,\x008\x001)]TJ
        # New: [ -61715(\x002\x00.\x006\x009\x008\x00.\x009\x008\x008\x00,\x008\x001)]TJ
        old_r58 = b"[ -62620(" + to_utf16_be("679.988,81") + b")]TJ"
        new_r58 = b"[ -61715(" + to_utf16_be(excel_saldos[58]) + b")]TJ"
        assert old_r58 in decomp, "Old pattern for Row 58 not found in Obj 411"
        decomp = decomp.replace(old_r58, new_r58, 1)
        
        return decomp

    update_stream(411, patch_411)
    print("Patched Obj 411 (Rows 47..58)")

    # 7. Patch Italic Page Numbers (Obj 11, 113, 213, 312, 411)
    page_objs = [11, 113, 213, 312, 411]
    page_offsets = {
        1: 555.77 - 542.40,
        2: 555.77 - 540.56,
        3: 555.77 - 540.52,
        4: 555.77 - 540.64,
        5: 555.77 - 540.44
    }
    for p_num, oid in enumerate(page_objs, 1):
        p_hex = f"{(0x30 + p_num):02X}"
        w_prefix = page_offsets[p_num]
        def make_patch_italic(pn, ph, w_off, obj_id):
            def _patch(decomp):
                m = re.search(rb'<00' + ph.encode() + rb'0020006F00660020(?:0036)?>\s*Tj(?:\s*/R1 8 Tf\s*1 0 0\.2 1 [\d\.]+ 0 Tm\s*<0036> Tj)?', decomp)
                if m:
                    repl = f"<00{ph}0020006F00660020> Tj\n/R1 8 Tf\n1 0 0.2 1 {w_off:.2f} 0 Tm\n<0036> Tj".encode()
                    decomp = decomp[:m.start()] + repl + decomp[m.end():]
                    print(f"Patched page {pn} italic page number in Obj {obj_id} (offset={w_off:.2f})")
                return decomp
            return _patch
        update_stream(oid, make_patch_italic(p_num, p_hex, w_prefix, oid))

    # 8. Reassemble full PDF with updated XRef table
    out = bytearray(header)
    for oid in top_objs:
        new_offset = len(out)
        rows[oid][1] = new_offset
        out.extend(obj_raw[oid])

    xref_start = len(out)
    rows[553][1] = xref_start

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

    xref_obj_str = b'553 0 obj\n<<' + new_xref_dict + b'>>\nstream\n' + comp_xref + b'\nendstream\nendobj\nstartxref\n' + str(xref_start).encode() + b'\n%%EOF\n'
    out.extend(xref_obj_str)

    with open(PDF_PATH, "wb") as f:
        f.write(out)

    print(f"Successfully patched and saved: {PDF_PATH} ({len(out)} bytes)")

if __name__ == "__main__":
    patch_keisya_saldos()
