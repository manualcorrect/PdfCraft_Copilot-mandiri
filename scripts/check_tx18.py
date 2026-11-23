import sys
import os
sys.path.append(os.path.abspath("src"))
sys.stdout.reconfigure(encoding='utf-8')
from parse_excel_template import parse_xara_excel_template

data = parse_xara_excel_template("templates/Galang_Jul_2026.xlsx")
tx18 = next(t for t in data["transactions"] if t.get("no") == 18)
print("Tx 18 in Excel:")
for k, v in tx18.items():
    print(f"  {k}: {repr(v)}")
