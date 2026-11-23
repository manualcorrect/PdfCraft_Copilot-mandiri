with open('src/parse_excel_template.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = """        elif p_name.startswith("5. RINGKASAN"):
            current_sec = "summary"
        else:"""

replacement = """        elif p_name.startswith("5. RINGKASAN"):
            current_sec = "summary"
        elif p_name.startswith("6.") or "SISTEM AUDIT" in p_name:
            current_sec = "audit"
        else:"""

if target in content:
    content = content.replace(target, replacement)
    with open('src/parse_excel_template.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated parse_excel_template.py for audit section successfully!")
else:
    print("Target not found!")
