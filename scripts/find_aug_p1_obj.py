import zlib
import re

with open('output/REK_KEISYA_AUG_OUTPUT_1.pdf', 'rb') as f:
    data = f.read()

# Find Obj 11
pat = re.compile(rb'11\s+0\s+obj\s*<<(.*?)>>\s*stream\r?\n(.*?)endstream', re.DOTALL)
m = pat.search(data)
if not m:
    print("Obj 11 not found by exact regex, searching all stream objects...")
    # Find all objects with stream
    for sm in re.finditer(rb'(\d+)\s+0\s+obj\s*<<(.*?)>>\s*stream\r?\n(.*?)endstream', data, re.DOTALL):
        obj_id = sm.group(1).decode()
        dict_text = sm.group(2).decode('latin1', errors='ignore')
        raw = sm.group(3)
        try:
            decomp = zlib.decompress(raw)
            if b'Saldo Awal' in decomp or b'298 667' in decomp:
                print(f"Found summary in Obj {obj_id} (len decomp={len(decomp)})")
        except Exception:
            pass
else:
    print("Found Obj 11!")
    dict_text = m.group(1).decode('latin1', errors='ignore')
    decomp = zlib.decompress(m.group(2))
    print("Obj 11 decompressed len:", len(decomp))
    with open('output/aug_p1_decompressed.txt', 'wb') as out_f:
        out_f.write(decomp)
    print("Saved to output/aug_p1_decompressed.txt")
