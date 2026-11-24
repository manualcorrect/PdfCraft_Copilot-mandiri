with open('scripts/build_keisya_okt_perfect.py', 'r', encoding='utf-8') as f:
    text = f.read()

print("File len:", len(text))
# Search for Tx descriptions or changed txs
for line in text.splitlines():
    if "Biaya administrasi" in line or "5411078192" in line or "desc_text =" in line:
        print(line)
