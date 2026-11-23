import os

path = 'src/parse_excel_template.py'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = """        # Format nominal & saldo
        if isinstance(nominal_raw, (int, float)):
            nominal = format_idr_currency(nominal_raw)
        else:
            nominal = str(nominal_raw or "").strip()

        if isinstance(saldo_raw, (int, float)):
            saldo = format_idr_currency(saldo_raw)
        else:
            saldo = str(saldo_raw or "").strip()

        tipe = str(tipe_raw or "").strip().upper()
        if not tipe:
            if isinstance(nominal_raw, (int, float)):
                tipe = "CR" if nominal_raw > 0 else "DB"
            elif nominal.startswith("+"):
                tipe = "CR"
            elif nominal.startswith("-"):
                tipe = "DB" """

# Normalize newlines
target_crlf = target.replace('\n', '\r\n')
target_lf = target.replace('\r\n', '\n')

replacement = """        tipe = str(tipe_raw or "").strip().upper()
        if not tipe:
            if isinstance(nominal_raw, (int, float)):
                tipe = "CR" if nominal_raw > 0 else "DB"
            elif str(nominal_raw or "").strip().startswith("+"):
                tipe = "CR"
            elif str(nominal_raw or "").strip().startswith("-"):
                tipe = "DB"

        # Format nominal & saldo
        if isinstance(nominal_raw, (int, float)):
            abs_curr = format_idr_currency(abs(nominal_raw))
            nominal = f"+{abs_curr}" if tipe == "CR" else f"-{abs_curr}"
        else:
            nom_str = str(nominal_raw or "").strip()
            if tipe == "CR" and not nom_str.startswith("+"):
                nominal = f"+{nom_str}"
            elif tipe == "DB" and not nom_str.startswith("-"):
                nominal = f"-{nom_str}"
            else:
                nominal = nom_str

        if isinstance(saldo_raw, (int, float)):
            saldo = format_idr_currency(abs(saldo_raw))
        else:
            saldo = str(saldo_raw or "").strip()"""

# Check which matches
if target_lf in text:
    text = text.replace(target_lf, replacement)
    print("Replaced LF version")
elif target_crlf in text:
    text = text.replace(target_crlf, replacement.replace('\n', '\r\n'))
    print("Replaced CRLF version")
else:
    # Try more flexible replacement
    print("Exact target not found, trying search")
    idx = text.find("# Format nominal & saldo")
    idx_end = text.find("# Date & Time formatting")
    if idx != -1 and idx_end != -1:
        text = text[:idx] + replacement.replace('\n', '\r\n' if '\r\n' in text else '\n') + "\n\n" + text[idx_end:]
        print("Replaced via index slice")
    else:
        print("Slice not found!")

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated parse_excel_template.py")
