with open('output/ref_p1_decompressed.txt', 'r', encoding='latin1') as f:
    text = f.read()

lines = text.split('\n')
print("=== LINES 210 to 320 ===")
for j in range(210, min(len(lines), 320)):
    print(f"{j}: {repr(lines[j])}")

print("\n=== LINES 425 to 475 ===")
for j in range(425, min(len(lines), 475)):
    print(f"{j}: {repr(lines[j])}")
