# Let's inspect the 37 descriptions and refine their multi-line breaks to match authentic Bank Mandiri formatting

descs = [
    # 01
    "Biaya transaksi bank\nPembayaran Danatopup\n89508089622130569",
    # 02
    "Pembayaran Danatopup\n89508089622130569",
    # 03
    "Pembayaran QR\nke SOTO AYAM LAMONGAN CAK JO\n601483798729",
    # 04
    "Penarikan tunai tanpa kartu\nDi ATM SRG AM PURI ANGREK 0\n089622130569",
    # 05
    "Biaya transfer BI Fast",
    # 06
    "Transfer BI Fast\nKe BCA\nBUDI SAPUTRA TANAGUN 1010570065",
    # 07
    "Transfer ke BANK MANDIRI\nMEI DWI LESTARI 1370011851231",
    # 08
    "Biaya transaksi bank\nPembayaran Danatopup\n89508087858621135",
    # 09
    "Pembayaran Danatopup\n89508087858621135",
    # 10
    "Transfer BI Fast\nDari BANK BNI\nFITRIANA PURWANINGSI 0314467254",
    # 11
    "Pembayaran QR\nke MAKO CAKE BAKERY SE 603\n601129029297",
    # 12
    "Pembayaran QR\nke RESERVE SA SERANG 1 1324\n601120346341",
    # 13
    "Biaya transaksi bank\nPembayaran Danatopup\n89508089622130569",
    # 14
    "Pembayaran Danatopup\n89508089622130569",
    # 15
    "Transfer dari BANK MANDIRI\nNANDA FEBRIANTI 1370013797036",
    # 16
    "Biaya transaksi bank\nPembayaran Danatopup\n89508089622130569",
    # 17
    "Pembayaran Danatopup\n89508089622130569",
    # 18
    "Pembayaran QR\nke PECEL LELE Mas Dikky, pas\n601580938038",
    # 19
    "Pembayaran QR\nke Syarkawi\n601581102500",
    # 20
    "Biaya transaksi bank\nPembayaran Danatopup\n89508083175718201",
    # 21
    "Pembayaran Danatopup\n89508083175718201",
    # 22 (Salary)
    "Transfer BI Fast\nDari BCA\nPT BENDI NASHA NIAGA INDUSTRI 5411078192\n(CENAIDJA)",
    # 23
    "Pembayaran QR\nke TEMAN DENTAL AHMAD YAN 40\n601208674693",
    # 24
    "Biaya transaksi bank\nPembayaran Danatopup\n89508089622130569",
    # 25
    "Pembayaran Danatopup\n89508089622130569",
    # 26
    "Penarikan tunai di ATM BANK\nMANDIRI SRG IM CIRUAS 01",
    # 27
    "Penarikan tunai tanpa kartu\nDi ATM SRG MD CIRUAS 01\n089622130569",
    # 28
    "Transfer BI Fast\nDari BANK BNI\nKARINA AMALIA DARMAW 1921323326",
    # 29
    "Pembayaran QR ke\nwarung madura\n506115913713",
    # 30
    "Penarikan tunai di ATM BANK\nMANDIRI SRG IM CIRUAS 01",
    # 31
    "Transfer BI Fast\nDari BCA\nMULYATI 2452705525\n-",
    # 32
    "Pembayaran QR\nke SPBU 3442109 KM 68 B 36\n601275499757",
    # 33
    "Biaya transfer BI Fast\n-",
    # 34
    "Transfer BI Fast\nKe BCA\nLUKMAN 1011284251",
    # 35
    "Transfer BI Fast\nDari BCA\nFERNANDUS NAINGGOLAN 8690976766\n-",
    # 36
    "Penarikan tunai di ATM\nBANK MANDIRI SRG IM PAKUPATAN 01",
    # 37
    "Biaya administrasi rekening"
]

print(f"Total defined descriptions: {len(descs)}")
for i, d in enumerate(descs, 1):
    lines = d.split("\n")
    print(f"Tx {i:2d} ({len(lines)} lines): {' | '.join(lines)}")
