with open('output/ref_p1_decompressed.txt', 'r', encoding='latin1') as f:
    text = f.read()

lines = text.split('\n')
capturing = False
block = []
for i, line in enumerate(lines):
    if any(k in line for k in ['667', '644', '621', '597']):
        print(f"Line {i}: {line}")
        # print surrounding 5 lines
        start = max(0, i-4)
        end = min(len(lines), i+6)
        print("--- CONTEXT ---")
        for j in range(start, end):
            print(f"{j}: {lines[j]}")
        print("---------------")
