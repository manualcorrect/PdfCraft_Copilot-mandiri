with open('output/aug_p1_decompressed.txt', 'r', encoding='latin1') as f:
    text = f.read()

idx_val = text.find('505.96 667 cm')
idx_tab = text.find('16 676 cm')

print(f"idx_val: {idx_val}, idx_tab: {idx_tab}")
print("--- RAW BLOCK 2 ---")
print(repr(text[idx_val-20:idx_tab+50]))
