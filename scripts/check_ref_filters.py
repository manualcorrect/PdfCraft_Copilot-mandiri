import re

ref_pdf = r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\.user_uploaded\media_1794538873844_ae928147.pdf"

with open(ref_pdf, "rb") as f:
    b = f.read()

# Check headers of all stream objects
for m in re.finditer(rb'(\d+)\s+0\s+obj\s*<<(.*?)>>\s*stream', b):
    oid = int(m.group(1))
    header = m.group(2).decode('latin1', errors='ignore')
    if "/Filter" in header or "/Type" in header:
        print(f"OID {oid}: {header[:120]}")
