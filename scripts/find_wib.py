import os

for root, dirs, files in os.walk("."):
    for f in files:
        if f.endswith(".py"):
            path = os.path.join(root, f)
            try:
                with open(path, "r", encoding="utf-8") as fp:
                    content = fp.read()
                    if "WIB" in content:
                        print(f"Found WIB in {path}")
            except:
                pass
