import re
import zlib

pdf_path = r"output/REK_KEISYA_SEP_OUTPUT_1.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

objs = re.findall(rb'(\d+)\s+0\s+obj', pdf_bytes)
print("Objects found:", [int(x) for x in objs])

for m in re.finditer(rb'(\d+)\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL):
    oid = int(m.group(1))
    stream_data = m.group(3)
    try:
        decomp = zlib.decompress(stream_data)
        has_wib = b"WIB" in decomp
        has_saldo = b"0.07451" in decomp or b"779.988" in decomp or b"127.488" in decomp or b"1.821.488" in decomp
        print(f"Obj {oid}: decomp len={len(decomp)}, WIB={has_wib}, saldo={has_saldo}")
        if has_wib:
            for s in [b"Saldo Awal", b"Syarat dan Ketentuan", b"KEISYA", b"ROY"]:
                if s in decomp:
                    print(f"  contains: {s}")
    except Exception as e:
        print(f"Obj {oid}: decomp failed ({e})")
