import zlib
import re

with open('output/REK_KEISYA_OKT_OUTPUT_1.pdf', 'rb') as f:
    data = f.read()

m = re.search(rb'\b12\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', data, re.DOTALL)
decomp = zlib.decompress(m.group(2)).decode('latin1', errors='ignore')

# Search for the OKT values: 6.850.820 or 14.306 or 8.446 or 12.710
for val in ['6.850', '14.306', '8.446', '12.710']:
    hex_v = ''.join(f'{ord(c):04X}' for c in val)
    idx = decomp.find(hex_v)
    print(f"OKT val {val} (hex={hex_v}) at pos {idx}")
    if idx != -1:
        # print surrounding
        print(repr(decomp[idx-100:idx+200]))
