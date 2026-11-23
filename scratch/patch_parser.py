with open('src/parse_excel_template.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = """    # Helper for currency formatting
    def format_idr_currency(val):
        if val is None:
            return ""
        if isinstance(val, (int, float)):
            return f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return str(val).strip()"""

replacement = """    # Helper for robust currency formatting (supports -Rp 7.651.988,00, -7.651.988,00, negative ints, etc.)
    import re
    def format_idr_currency(val):
        if val is None:
            return ""
        if isinstance(val, (int, float)):
            abs_val = abs(val)
            return f"{abs_val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        s = str(val).strip()
        s_clean = re.sub(r'[^\\d,\\.]', '', s)
        if not s_clean:
            return s
        if "," in s_clean:
            parts = s_clean.split(",")
            integer_part = parts[0].replace(".", "")
            decimal_part = parts[1] if len(parts) > 1 else "00"
            try:
                num_val = float(f"{integer_part}.{decimal_part}")
            except:
                num_val = 0.0
        elif "." in s_clean:
            parts = s_clean.split(".")
            if len(parts[-1]) == 2:
                try:
                    num_val = float(s_clean)
                except:
                    num_val = 0.0
            else:
                try:
                    num_val = float("".join(parts))
                except:
                    num_val = 0.0
        else:
            try:
                num_val = float(s_clean)
            except:
                return s
        return f"{num_val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")"""

if target in content:
    content = content.replace(target, replacement)
    with open('src/parse_excel_template.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated src/parse_excel_template.py successfully!")
else:
    # Try normalizing line endings
    content_norm = content.replace("\r\n", "\n")
    target_norm = target.replace("\r\n", "\n")
    if target_norm in content_norm:
        content_norm = content_norm.replace(target_norm, replacement)
        with open('src/parse_excel_template.py', 'w', encoding='utf-8') as f:
            f.write(content_norm.replace("\n", "\r\n"))
        print("Updated src/parse_excel_template.py successfully (normalized)!")
    else:
        print("Target not found!")
