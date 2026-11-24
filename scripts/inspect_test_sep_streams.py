import re, zlib

with open('output/test_sep_p3.pdf', 'rb') as f:
    data = f.read()

print("File length:", len(data))
sx = re.findall(rb'startxref[\r\n]+(\d+)', data)
print("startxref:", sx)

# Check content streams
for m in re.finditer(rb'(\d+)\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', data, re.DOTALL):
    oid = int(m.group(1))
    dict_part = m.group(2)
    stream_part = m.group(3)
    try:
        dec = zlib.decompress(stream_part)
        if b"0.07451 0.294118 0.729412 rg/R2 8 Tf" in dec:
            print(f"Page table stream OID: {oid} (len {len(dec)})")
        elif b"Menara Mandiri" in dec:
            print(f"Header stream OID: {oid} (len {len(dec)})")
        elif b"Saldo Awal" in dec:
            print(f"Summary box stream OID: {oid} (len {len(dec)})")
    except:
        pass
