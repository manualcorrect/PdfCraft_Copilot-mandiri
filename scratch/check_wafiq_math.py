import openpyxl

wb = openpyxl.load_workbook(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\aug\Template_Mutasi_AUG.xlsx", data_only=True)
ws = wb["Tabel_Mutasi"]
credits = 0.0
debits = 0.0
saldo_awal = 4784795.0
running = saldo_awal

has_error = False
for r in range(6, ws.max_row + 1):
    nom = ws.cell(r, 5).value
    saldo = ws.cell(r, 7).value
    if nom is not None and str(nom) != "-":
        nom = float(nom)
        saldo = float(saldo)
        if nom > 0:
            credits += nom
        else:
            debits += abs(nom)
        running += nom
        if abs(running - saldo) > 0.01:
            print(f"Row {r}: CALC ERROR! running={running:,.2f} != recorded={saldo:,.2f}")
            has_error = True

print(f"Total Credits: {credits:,.2f}")
print(f"Total Debits:  {debits:,.2f}")
print(f"Saldo Awal:    {saldo_awal:,.2f}")
print(f"Calculated Saldo Akhir: {running:,.2f}")
s1_sa = wb["Header & Ringkasan"]["B22"].value
s1_dm = wb["Header & Ringkasan"]["B23"].value
s1_dk = wb["Header & Ringkasan"]["B24"].value
s1_sk = wb["Header & Ringkasan"]["B25"].value
print(f"Header Sheet: Saldo Awal={s1_sa}, Dana Masuk={s1_dm}, Dana Keluar={s1_dk}, Saldo Akhir={s1_sk}")
print("Rolling Balance Consistent:", not has_error)
print("Balance Formula Valid:", abs((saldo_awal + credits - debits) - running) < 0.01)
