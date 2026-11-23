import pypdf
import zlib
import re

user_ref_path = r'C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\.user_uploaded\media_1794538873844_ae928147.pdf'

reader = pypdf.PdfReader(user_ref_path)
page0 = reader.pages[0]
contents = page0.get_contents()

if isinstance(contents, list):
    stream_bytes = b"".join(c.get_data() for c in contents)
else:
    stream_bytes = contents.get_data()

text = stream_bytes.decode('latin1', errors='ignore')

# Search for the summary box section
# Look for 298 or Saldo Awal or 667
match = re.search(r'q\s*298\s+667\s+cm.*?(?=Q\s*q|\Z)', text, re.DOTALL)
if match:
    print("Found summary block with 298 667 cm:")
    print(match.group(0)[:1500])
else:
    # search for 'Saldo' or 'Dana'
    print("Searching for BT blocks around y=667, 644, 621, 597:")
    matches = re.findall(r'BT[\s\S]*?ET', text)
    for m in matches:
        if any(w in m for w in ['Saldo', 'Dana', 'Keluar', 'Masuk', '16.827', '18.273', '52.488', '1.498']):
            print("--- BT BLOCK ---")
            print(m)
