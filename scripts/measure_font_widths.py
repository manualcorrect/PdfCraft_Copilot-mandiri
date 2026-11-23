import pdfplumber
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

with pdfplumber.open('templates/master_page_1.pdf') as pdf:
    char_widths = defaultdict(list)
    for c in pdf.pages[0].chars:
        if c['top'] > 300 and c['top'] < 800:
            char_widths[c['text']].append((c['width'], c['fontname'], c['size']))

print("=== Character widths in transaction table ===")
for ch in sorted(char_widths.keys()):
    widths = [w[0] for w in char_widths[ch]]
    avg_w = sum(widths) / len(widths)
    font = char_widths[ch][0][1]
    size = char_widths[ch][0][2]
    print(f"'{ch}': width={avg_w:.4f} (font={font}, size={size:.2f})")
