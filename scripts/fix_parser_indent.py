with open('src/parse_excel_template.py', 'r', encoding='utf-8') as f:
    text = f.read()

bad = """                tipe = str(tipe_raw or "").strip().upper()
        if not tipe:"""

good = """        tipe = str(tipe_raw or "").strip().upper()
        if not tipe:"""

text = text.replace(bad, good)
text = text.replace("# Date & Time formatting", "        # Date & Time formatting")

with open('src/parse_excel_template.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Indentation fixed.")
