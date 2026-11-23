import re
import zlib

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

def u16(s): return s.encode("utf-16-be")

page_objs = {1: 402, 2: 1, 3: 102, 4: 203, 5: 304}

for p_num, oid in page_objs.items():
    m = re.search(rb'\b' + str(oid).encode() + rb'\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
    decomp = zlib.decompress(m.group(2))
    print(f"\n================ Page {p_num} (Obj {oid}) Header/Summary ================")
    
    targets = ["ROY", "Jakarta", "Mar", "09 Sep", "1650003584860", "1.498.768", "16.827.000", "18.273.280", "52.488"]
    for t in targets:
        u = u16(t)
        for match in re.finditer(re.escape(u), decomp):
            start = max(0, match.start() - 60)
            end = min(len(decomp), match.end() + 80)
            print(f"  Target '{t}': {decomp[start:end]}")
