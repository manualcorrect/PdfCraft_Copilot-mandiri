import pypdfium2 as pdfium
import zlib
import re

ref_pdf = r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\.user_uploaded\media_1794538873844_ae928147.pdf"

with open(ref_pdf, "rb") as f:
    b = f.read()

# Find page 1 contents
# Find /Type /Page
m_p1 = re.search(rb'/Type\s*/Page\b.*?/Contents\s+(\d+)\s+0\s+R', b, re.DOTALL)
if m_p1:
    c_oid = int(m_p1.group(1))
    print(f"Page 1 /Contents OID: {c_oid}")
    m_stream = re.search(rb'\b' + str(c_oid).encode() + rb'\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', b, re.DOTALL)
    dec = zlib.decompress(m_stream.group(2))
    print("Page 1 stream decompressed length:", len(dec))
    
    # Let's extract all text operators (BT ... ET)
    bts = list(re.finditer(rb'BT(.*?)ET', dec, re.DOTALL))
    print(f"Found {len(bts)} BT blocks in Page 1.")
    for i, bt in enumerate(bts):
        content = bt.group(0)
        # check if it relates to summary box (y around 590..680 in PDF coordinates)
        # In PDF coords: 842 - 168.92 = 673.08; 842 - 238.92 = 603.08
        if any(w in content for w in [b"Saldo", b"\x00S\x00a", b"Dana", b"\x00D\x00a", b"1.498", b"\x001\x00.\x004", b"16.827", b"18.273", b"52.488"]):
            print(f"\n--- BT Block #{i+1} ---")
            print(content.decode('latin1', errors='ignore'))
