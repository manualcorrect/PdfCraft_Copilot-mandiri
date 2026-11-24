import re
import zlib

pdf_path = r'c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output\test_p46.pdf'
with open(pdf_path, 'rb') as f:
    pdf_bytes = f.read()

# find obj 10 0 obj
m_obj = re.search(rb'\b10\s+0\s+obj\s*<<(.*?)>>\s*stream(\r\n|\n)', pdf_bytes)
dict_data = m_obj.group(1)
m_len = re.search(rb'/Length\s+(\d+)', dict_data)
length = int(m_len.group(1))
stream_start = m_obj.end()
stream_data = pdf_bytes[stream_start : stream_start + length]
dec = zlib.decompress(stream_data).decode('latin1', errors='ignore')

# inspect colons and labels
pos_c1 = dec.find('446.12 667')
print(f"pos_c1: {pos_c1}")
if pos_c1 != -1:
    print("Dec snippet around colons:")
    print(dec[pos_c1-100 : pos_c1+300])

pos_now = dec.find('16 676 cm')
print(f"\npos_now: {pos_now}")
if pos_now != -1:
    print("Dec snippet before 16 676 cm:")
    print(dec[pos_now-400 : pos_now+50])
