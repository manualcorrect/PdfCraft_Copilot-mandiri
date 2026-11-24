bold_w = {
    '1': 3.16015625, '2': 4.76171875, '3': 4.83984375, '4': 4.87890625, '5': 4.83984375,
    '6': 4.87890625, '7': 4.3203125, '8': 4.9609375, '9': 4.87890625, '0': 5.4375,
    '.': 1.83984375, ',': 1.83984375, ' ': 1.83984375, '+': 4.83984375, '-': 3.16015625,
    'd': 4.9609375, 'a': 4.4375, 'r': 3.23828125, 'i': 2.078125, 'o': 4.71875, 'f': 2.6796875
}

def get_bold_width(s):
    return sum(bold_w[c] for c in s)

values = [
    ("Saldo Awal", "5.730.669,81", 667),
    ("Dana Masuk", "+ 11.408.000,00", 644),
    ("Dana Keluar", "- 5.669.669,00", 621),
    ("Saldo Akhir", "11.469.000,81", 597)
]

print("October Summary Box Value Positions (Right edge 567.00 pt):")
for label, val, y in values:
    w = get_bold_width(val)
    x0 = 567.00 - w
    print(f"  {label:<12}: '{val}' | width={w:.2f} pt | x0={x0:.2f} pt | Y={y} pt")
