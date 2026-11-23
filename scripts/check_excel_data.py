import sys
import os
sys.path.append(os.path.abspath("src"))
sys.stdout.reconfigure(encoding='utf-8')
from parse_excel_template import parse_xara_excel_template

data = parse_xara_excel_template("templates/Galang_Jul_2026.xlsx")
print(f"Header: {data['header']}")
print(f"Summary: {data['summary']}")
print(f"Transactions count: {len(data['transactions'])}")
for i, tx in enumerate(data['transactions'][:12]):
    print(f"  Tx #{i+1:2d}: No={tx.get('no')} Date={tx.get('tanggal')} {tx.get('jam')} Nom={tx.get('nominal')} Saldo={tx.get('saldo')} Desc={repr(tx.get('uraian'))}")
