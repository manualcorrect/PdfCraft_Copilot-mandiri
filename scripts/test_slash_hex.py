def to_hex(text):
    return ''.join(f'{ord(c):04X}' for c in text)

print("Saldo Awal/:", to_hex("Saldo Awal/"))
print("Initial Balance:", to_hex("Initial Balance"))
print("Dana Masuk/:", to_hex("Dana Masuk/"))
print("Incoming Transactions:", to_hex("Incoming Transactions"))
print("Dana Keluar/:", to_hex("Dana Keluar/"))
print("Outgoing Transactions:", to_hex("Outgoing Transactions"))
print("Saldo Akhir/:", to_hex("Saldo Akhir/"))
print("Closing Balance:", to_hex("Closing Balance"))
