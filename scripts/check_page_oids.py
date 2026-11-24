import re, zlib

with open('output/test_sep_p3.pdf', 'rb') as f:
    data = f.read()

oids = [10, 113, 212, 311, 411]
for oid in oids:
    m = re.search(rb'\b' + str(oid).encode() + rb'\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', data, re.DOTALL)
    if m:
        stream_data = m.group(2)
        dec = zlib.decompress(stream_data)
        has_table = b"0.07451 0.294118 0.729412 rg/R2 8 Tf" in dec
        print(f"OID {oid}: decompressed len = {len(dec)}, has_table = {has_table}")
    else:
        print(f"OID {oid} NOT FOUND")
