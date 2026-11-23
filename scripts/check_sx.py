import re

with open(r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output\REK_KEISYA_OKT_OUTPUT_1.pdf", "rb") as f:
    b = f.read()

m = re.search(rb'startxref\s+(\d+)', b)
sx = int(m.group(1))
print("startxref:", sx)
print("Bytes at startxref:")
print(b[sx:sx+200])
