import re
import zlib

with open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\0.pdf", "rb") as f:
    pdf_bytes = f.read()

# find obj 609
m = re.search(rb'\b609\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
if m:
    dict_part = m.group(1).decode('latin1')
    stream_part = m.group(2)
    decomp = zlib.decompress(stream_part).decode('latin1')
    print("Found obj 609, stream length decompressed:", len(decomp))
    
    # check pos_c1, pos_c4
    pos_c1 = decomp.find('446.12 667')
    pos_c4 = decomp.find('446.12 597')
    start_b1 = decomp.rfind('q', 0, pos_c1)
    m_end_b1 = re.search(r'ET\s*Q', decomp[pos_c4:])
    end_b1 = pos_c4 + m_end_b1.end() if m_end_b1 else -1
    print(f"start_b1={start_b1}, pos_c1={pos_c1}, pos_c4={pos_c4}, end_b1={end_b1}")
    
    pos_now = decomp.find('16 676 cm')
    end_b2 = decomp.rfind('q', 0, pos_now)
    matches = list(re.finditer(r'q\s+1\s+0\s+0\s+1\s+[\d\.]+\s+667\s+cm', decomp[end_b1:end_b2]))
    print(f"pos_now={pos_now}, end_b2={end_b2}, matches len={len(matches)}")
    if matches:
        print(f"start_b2={end_b1 + matches[-1].start()}")
        print("Slice of b2:")
        print(decomp[end_b1 + matches[-1].start() : end_b2][:200])
else:
    print("Obj 609 not found!")
