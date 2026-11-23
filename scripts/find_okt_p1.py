import re
import zlib

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\okt\0.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

def u16(s): return s.encode("utf-16-be")

content_oids = []
for m in re.finditer(rb'(\d+)\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL):
    oid = int(m.group(1))
    stream_data = m.group(3)
    try:
        decomp = zlib.decompress(stream_data)
        if u16("Menara Mandiri") in decomp:
            print(f"Content stream found: Obj {oid}")
            content_oids.append(oid)
    except:
        pass

print("All content stream OIDs with Menara Mandiri:", content_oids)
