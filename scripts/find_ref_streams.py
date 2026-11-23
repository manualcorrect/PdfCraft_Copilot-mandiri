import zlib
import re

pdf_path = r'C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\.user_uploaded\media_1794538873844_ae928147.pdf'

with open(pdf_path, 'rb') as f:
    data = f.read()

# Find all streams
stream_pattern = re.compile(rb'stream\r?\n(.*?)endstream', re.DOTALL)
streams = []
for m in stream_pattern.finditer(data):
    raw = m.group(1)
    try:
        decomp = zlib.decompress(raw)
        streams.append(decomp)
    except Exception:
        try:
            decomp = zlib.decompress(raw, -15)
            streams.append(decomp)
        except Exception:
            pass

print(f"Decompressed {len(streams)} streams.")
for i, s in enumerate(streams):
    text = s.decode('latin1', errors='ignore')
    if 'Saldo Awal' in text or 'Dana Keluar' in text or '18.273.280' in text:
        print(f"\n--- Stream {i} contains summary text --- (len={len(text)})")
        lines = text.split('\n')
        for line in lines:
            if any(k in line for k in ['Saldo', 'Dana', '18.273', '16.827', '52.488', '1.498', 'Initial', 'Outgoing', 'Incoming', 'Closing', '446.12', '567']):
                print(line)
