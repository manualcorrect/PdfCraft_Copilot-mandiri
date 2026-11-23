import re
import zlib

pdf_path = r"output/REK_KEISYA_SEP_OUTPUT_1.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

page_content_oids = {1: 10, 2: 113, 3: 212, 4: 311, 5: 410}

for p_num, oid in page_content_oids.items():
    m = re.search(rb'\b' + str(oid).encode() + rb'\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
    decomp = zlib.decompress(m.group(2))
    print(f"\n================ Page {p_num} (Obj {oid}) ================")
    for b in re.finditer(rb'q\s+1\s+0\s+0\s+1\s+([\d\.]+)\s+([\d\.]+)\s+cm\s+BT\s+(.*?)\s+ET\s+Q', decomp, re.DOTALL):
        x = float(b.group(1))
        y = float(b.group(2))
        if 500 <= x <= 580 and 715 <= y <= 745:
            # find strings
            strings = re.findall(rb'\(([^\)]*)\)', b.group(3))
            text_repr = []
            for s in strings:
                try:
                    text_repr.append(s.decode('utf-16-be'))
                except:
                    text_repr.append(str(s))
            print(f"  x={x:.2f}, y={y:.2f}: {b.group(0)}")
            print(f"    Decoded: {' | '.join(text_repr)}")
