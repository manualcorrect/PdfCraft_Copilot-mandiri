import sys
import os
sys.path.append(os.path.abspath("src"))
sys.path.append(os.path.abspath("."))
sys.stdout.reconfigure(encoding='utf-8')
from description_training_system.description_model import DescriptionModelEngine

test_inputs = [
    # As in Excel Galang Jul
    "Transfer BI Fast Dari BCA\nPT BENDI NASHA NIAGA INDUSTRI 5411078192\n(CENAIDJA)",
    # Flattened
    "Transfer BI Fast Dari BCA PT BENDI NASHA NIAGA INDUSTRI 5411078192 (CENAIDJA)",
    # Already 4 lines
    "Transfer BI Fast\nDari BCA\nPT BENDI NASHA NIAGA INDUSTRI 5411078192\n(CENAIDJA)"
]

print("=== TESTING TX 18 FORMATTING ===")
for inp in test_inputs:
    res = DescriptionModelEngine.format(inp)
    print(f"\nInput: {repr(inp)}")
    print(f"Category: {res['category']}, Lines count: {res['line_count']}, Offset: {res['target_top_offset']}")
    for i, l in enumerate(res['lines']):
        print(f"  Line {i+1}: {repr(l)}")
