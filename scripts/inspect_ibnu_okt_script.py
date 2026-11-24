with open('scripts/build_ibnu_okt_final.py', 'r', encoding='utf-8') as f:
    text = f.read()

for line in text.splitlines():
    if "active_row_count ==" in line or "desc_text =" in line or "Biaya administrasi" in line or "5411078192" in line:
        print(line)
