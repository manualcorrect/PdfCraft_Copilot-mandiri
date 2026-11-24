import os
import re

for root, dirs, files in os.walk("scripts"):
    for f in files:
        if f.endswith(".py") and ("build" in f or "perfect" in f or "final" in f):
            p = os.path.join(root, f)
            with open(p, "r", encoding="utf-8", errors="ignore") as fh:
                c = fh.read()
                m = re.findall(r"(?:BENDI|CENAIDJA|5411078192|UPAH|GAJI|Payroll).*?", c)
                if m:
                    print(f"File {f}:")
                    for line in c.split("\n"):
                        if any(k in line for k in ["BENDI", "CENAIDJA", "5411078192", "UPAH", "GAJI"]):
                            print(f"   {line.strip()}")
