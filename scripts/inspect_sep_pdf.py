with open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf", "rb") as f:
    pdf_bytes = f.read()

import re, zlib

obj_matches = re.finditer(rb'(\d+)\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
for m in obj_matches:
    oid = m.group(1).decode()
    stream_data = m.group(3)
    try:
        decomp = zlib.decompress(stream_data)
        has_wib = b"WIB" in decomp or b"\x00W\x00I\x00B" in decomp
        saldos = re.findall(rb'\[\s*(-?\d+)\s*\(([\x00\d\.,]+)\)\s*\]TJ', decomp)
        print(f"Obj {oid}: decomp len={len(decomp)}, WIB={has_wib}, Saldo count={len(saldos)}")
        for k, s in saldos:
            s_clean = s.replace(b"\x00", b"").decode("latin1")
            if any(c in s_clean for c in [",", "."]) and len(s_clean) >= 6:
                print(f"   k={k.decode():<6} s={s_clean}")
    except Exception as e:
        pass
