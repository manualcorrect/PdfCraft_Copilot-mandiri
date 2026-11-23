import re
import zlib
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output\test_step3.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

oid = 412
m = re.search(rb'\b' + str(oid).encode() + rb'\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
decomp = zlib.decompress(m.group(2))

# Find all occurrences of 0.07451 0.294118 0.729412
saldo_matches = list(re.finditer(rb'0\.07451\s+0\.294118\s+0\.729412\s+rg/R2\s+8\s+Tf.*?(?:TJ|Tj)', decomp, re.DOTALL))
print(f"Total saldo markers in Page 5 decomp: {len(saldo_matches)}")

for i, sm in enumerate(saldo_matches):
    start = max(0, sm.start() - 150)
    end = min(len(decomp), sm.end() + 50)
    print(f"\n--- Saldo {i+1} ---")
    print(decomp[start:end])
