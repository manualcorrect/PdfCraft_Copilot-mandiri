import zlib
import re

pdf_path = r'C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\.user_uploaded\media_1794538873844_ae928147.pdf'

with open(pdf_path, 'rb') as f:
    data = f.read()

# Let's inspect Page 1 object to find its /Contents
# Find page object
page_matches = re.findall(rb'(\d+)\s+(\d+)\s+obj\s*<<([^>]*/Type\s*/Page[^>]*)>>', data)
print("Found pages:", len(page_matches))
for num, gen, content in page_matches:
    print(f"Page obj {num.decode()}: {content.decode('latin1', errors='ignore')[:300]}")
    break

# Find Contents obj
p0_match = re.search(rb'(\d+)\s+\d+\s+obj\s*<<[^>]*?/Type\s*/Page.*?/Contents\s+(\d+)\s+\d+\s+R', data, re.DOTALL)
if p0_match:
    contents_id = p0_match.group(2)
    print(f"Page 1 Contents object ID: {contents_id.decode()}")
    
    # Extract that object
    obj_pattern = re.compile(rb'' + contents_id + rb'\s+\d+\s+obj\s*<<(.*?)>>\s*stream\r?\n(.*?)endstream', re.DOTALL)
    m = obj_pattern.search(data)
    if m:
        dict_part = m.group(1)
        raw_stream = m.group(2)
        print("Dict part:", dict_part.decode('latin1', errors='ignore'))
        decomp = zlib.decompress(raw_stream)
        print("Decompressed stream length:", len(decomp))
        with open('output/ref_p1_decompressed.txt', 'wb') as out_f:
            out_f.write(decomp)
        print("Written to output/ref_p1_decompressed.txt")
