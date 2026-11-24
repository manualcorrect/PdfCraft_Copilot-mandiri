import re, zlib
from test_xref_sep import obj_raw, top_objs

raw113 = obj_raw.get(113)
if raw113:
    print("Raw 113 header:")
    print(raw113[:200])
    m_s = re.search(rb'stream[\r\n]+(.*?)[\r\n]+endstream', raw113, re.DOTALL)
    if m_s:
        stream_bytes = m_s.group(1)
        print("Stream bytes len:", len(stream_bytes))
        try:
            dec = zlib.decompress(stream_bytes)
            print("Decompressed len:", len(dec))
            print("Decompressed snippet:", dec[:200])
        except Exception as e:
            print("Decompress error:", e)
else:
    print("OID 113 not in obj_raw!")
    print("top_objs around 113:", [oid for oid in top_objs if 100 <= oid <= 130])
