with open('output/aug_p1_decompressed.txt', 'r', encoding='latin1') as f:
    text = f.read()

import re

# Find colon block for Saldo Awal (446.12 667 cm)
# Find label block (298 667 cm)
# Find colon block for Saldo Akhir (446.12 597 cm)
# Find value block (505.96 667 cm)

print("--- SEARCHING SUMMARY ELEMENTS IN AUG STREAM ---")
pos_c1 = text.find('446.12 667 cm')
pos_lbl = text.find('298 667 cm')
pos_c4 = text.find('446.12 597 cm')
pos_vals = text.find('505.96 667 cm')

print(f"Colon 1 pos: {pos_c1}")
print(f"Labels pos: {pos_lbl}")
print(f"Colon 4 pos: {pos_c4}")
print(f"Values pos: {pos_vals}")

# Let's see what surrounds them:
# 1. Colon 1 & Labels & Colon 4
start_block1 = text.rfind('q', 0, pos_c1)
end_block1 = text.find('Q', pos_c4) + 1
print(f"\nBlock 1 (Colons & Labels) [{start_block1}:{end_block1}]:")
print(repr(text[start_block1:end_block1]))

# 2. Values
start_block2 = text.rfind('q', 0, pos_vals)
# find where values end before Tabungan NOW
pos_now = text.find('Tabungan')
if pos_now == -1:
    pos_now = text.find('T a b u n g a n')
end_block2 = text.rfind('q', 0, pos_now)
print(f"\nBlock 2 (Values) [{start_block2}:{end_block2}]:")
print(repr(text[start_block2:end_block2]))
