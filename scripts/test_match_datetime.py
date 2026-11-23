import re
import zlib

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

page_objs = {1: 402, 2: 1, 3: 102, 4: 203, 5: 304}
expected = {1: 10, 2: 12, 3: 12, 4: 12, 5: 4}

# Date regex
date_re = re.compile(rb'(q\s+1\s+0\s+0\s+1\s+(?:51\.\d+|52(?:\.0+)?)\s+([\d\.]+)\s+cm\s+BT\s+0\s+0\s+0\s+rg/R1\s+8\s+Tf(/R\d+\s+gs)\(([^\)]*?\x00M\x00a\x00r\x00[^\)]*?)\)\s*Tj\s+ET\s+Q)')

# Time regex
time_re = re.compile(rb'(q\s+1\s+0\s+0\s+1\s+(?:51\.\d+|52(?:\.0+)?)\s+([\d\.]+)\s+cm\s+BT\s+0\s+0\s+0\s+rg/R1\s+8\s+Tf(/R\d+\s+gs)\(([^\)]*?\x00W\x00I\x00B)\)\s*Tj\s+ET\s+Q)')

for p_num, oid in page_objs.items():
    m = re.search(rb'\b' + str(oid).encode() + rb'\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
    decomp = zlib.decompress(m.group(2))
    
    dates = sorted(list(date_re.finditer(decomp)), key=lambda x: float(x.group(2)), reverse=True)
    times = sorted(list(time_re.finditer(decomp)), key=lambda x: float(x.group(2)), reverse=True)
    
    print(f"Page {p_num} (Obj {oid}): found {len(dates)} dates, {len(times)} times (expected {expected[p_num]})")
    for i in range(len(dates)):
        d_text = dates[i].group(4).decode('utf-16-be', 'ignore')
        t_text = times[i].group(4).decode('utf-16-be', 'ignore') if i < len(times) else "MISSING"
        print(f"  Row {i+1:2d}: Date='{d_text}', Time='{t_text}'")
