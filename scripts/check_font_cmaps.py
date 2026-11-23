import zlib
import re

with open('output/REK_KEISYA_AUG_OUTPUT_1.pdf', 'rb') as f:
    data = f.read()

# Find font objects 109, 110, 111
for fid in [109, 110, 111]:
    pat = re.compile(rb'' + str(fid).encode() + rb'\s+\d+\s+obj\s*<<(.*?)>>', re.DOTALL)
    m = pat.search(data)
    if m:
        print(f"Font obj {fid}: {m.group(1).decode('latin1', errors='ignore')}")

# Check obj 437, 441, 444 (CMaps)
for cid in [437, 441, 444]:
    pat = re.compile(rb'' + str(cid).encode() + rb'\s+\d+\s+obj\s*<<(.*?)>>\s*stream\r?\n(.*?)endstream', re.DOTALL)
    m = pat.search(data)
    if m:
        raw = m.group(2)
        try:
            decomp = zlib.decompress(raw)
            print(f"\nCMap {cid} (len={len(decomp)}):")
            print(decomp.decode('latin1', errors='ignore')[:300])
        except Exception as e:
            print(f"CMap {cid} decompress error: {e}")
