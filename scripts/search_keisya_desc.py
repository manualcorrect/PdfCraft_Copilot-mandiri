with open('scripts/build_keisya_okt_perfect.py', 'r', encoding='utf-8') as f:
    text = f.read()

for i, line in enumerate(text.splitlines()):
    if "desc" in line.lower() or "keterangan" in line.lower():
        print(f"L{i+1}: {line}")
