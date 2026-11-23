import sys
import os
sys.path.append(os.path.abspath("src"))
sys.stdout.reconfigure(encoding='utf-8')
from harvest_authentic_descriptions import descriptions_catalog

print("=== ALL BI_FAST PATTERNS ===")
bi_fast_samples = [d for d in descriptions_catalog if "BI Fast" in d["full_text"] or "BI FAST" in d["full_text"]]
seen = set()
for b in bi_fast_samples:
    lines_tuple = tuple(b["lines"])
    if lines_tuple not in seen:
        seen.add(lines_tuple)
        print(f"\nSample from {b['file']} (Page {b['page']}, Row {b['row']}, Total {len(b['lines'])} lines):")
        for i, l in enumerate(b["lines"]):
            print(f"  Line {i+1}: {repr(l)}")
