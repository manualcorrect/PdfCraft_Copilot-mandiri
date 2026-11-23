import re, zlib

with open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf", "rb") as f:
    data = f.read()

pattern = re.compile(rb'(\d+)\s+(\d+)\s+obj\s*(<<.*?>>)\s*stream[\r\n]+(.*?)[\r\n]+endstream\s*endobj', re.DOTALL)
for m in pattern.finditer(data):
    obj_num = m.group(1).decode()
    dict_part = m.group(3).decode('latin1')
    stream_data = m.group(4)
    print(f"Obj {obj_num}: dict={dict_part[:80]} stream_len={len(stream_data)}")
    try:
        decomp = zlib.decompress(stream_data)
        if b"Menara Mandiri" in decomp or b"e-Statement" in decomp:
            print(f"  -> THIS IS A PAGE CONTENT STREAM! decomp_len={len(decomp)}")
    except:
        pass
