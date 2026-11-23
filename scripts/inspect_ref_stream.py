import pypdfium2 as pdfium
import re
import zlib

ref_pdf = r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\.user_uploaded\media_1794538873844_ae928147.pdf"

with open(ref_pdf, "rb") as f:
    b = f.read()

print("File size:", len(b))
# Let's find all obj streams
matches = list(re.finditer(rb'(\d+)\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', b, re.DOTALL))
print("Total streams:", len(matches))

for m in matches:
    oid = int(m.group(1))
    s = m.group(3)
    try:
        dec = zlib.decompress(s)
        if b"Saldo" in dec or b"\x00S\x00a\x00l\x00d\x00o" in dec:
            print(f"Found Saldo in stream OID {oid} (decomp len {len(dec)})!")
            # print all lines containing Saldo, Dana, or Keluar
            for line in dec.splitlines():
                if any(k in line for k in [b"Saldo", b"\x00S\x00a\x00l", b"Dana", b"\x00D\x00a\x00n\x00a", b"Keluar", b"\x00K\x00e\x00l"]):
                    print("   ", line[:150])
    except Exception as e:
        pass
