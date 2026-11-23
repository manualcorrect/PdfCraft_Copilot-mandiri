def to_utf16_hex(text):
    return ''.join(f'{ord(c):04X}' for c in text)

print("Saldo Awal:", to_utf16_hex("Saldo Awal"))
print("/Initial Balance:", to_utf16_hex("/Initial Balance"))
print("Dana Masuk:", to_utf16_hex("Dana Masuk"))
print("/Incoming Transactions:", to_utf16_hex("/Incoming Transactions"))
print("Dana Keluar:", to_utf16_hex("Dana Keluar"))
print("/Outgoing Transactions:", to_utf16_hex("/Outgoing Transactions"))
print("Saldo Akhir:", to_utf16_hex("Saldo Akhir"))
print("/Closing Balance:", to_utf16_hex("/Closing Balance"))
print("Colon:", to_utf16_hex(":"))
