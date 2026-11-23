import re
import zlib

with open("output/test_save.pdf", "rb") as f:
    pdf_bytes = f.read()

# Let's inspect all objects that are streams
for m in re.finditer(rb'(\d+)\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL):
    oid = int(m.group(1))
    dict_part = m.group(2).decode('latin1', errors='ignore')
    stream_data = m.group(3)
    try:
        decomp = zlib.decompress(stream_data)
        # Check if it contains "Saldo Awal" or "IBNU AGUN"
        if b"Saldo Awal" in decomp or b"IBNU AGUN" in decomp or b"446.12 667" in decomp:
            print(f"Match found! OID {oid} is Page 1 contents! Length decompressed: {len(decomp)}")
    except Exception as e:
        pass
