import openpyxl

excel_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\okt\Template_Mutasi_OKT.xlsx"
wb = openpyxl.load_workbook(excel_path, data_only=True)
print("Sheets:", wb.sheetnames)

ws1 = wb["Template_Mutasi"] if "Template_Mutasi" in wb.sheetnames else wb.worksheets[0]
print(f"\n--- Sheet 1: {ws1.title} ---")
for r in range(1, 35):
    row_vals = [ws1.cell(r, c).value for c in range(1, 15) if ws1.cell(r, c).value is not None]
    if row_vals:
        print(f"Row {r:2d}: {row_vals}")

ws2 = wb["Tabel_Mutasi"] if "Tabel_Mutasi" in wb.sheetnames else wb.worksheets[1]
print(f"\n--- Sheet 2: {ws2.title} ---")
active_rows = []
for r in range(1, 80):
    val_nom = ws2.cell(r, 5).value
    val_sal = ws2.cell(r, 7).value
    if val_nom is not None:
        try:
            f_nom = float(val_nom)
            f_sal = float(val_sal) if val_sal is not None else 0.0
            active_rows.append((r, ws2.cell(r, 1).value, ws2.cell(r, 2).value, ws2.cell(r, 3).value, f_nom, ws2.cell(r, 6).value, f_sal))
        except:
            print(f"Header/Text Row {r:2d}: {[ws2.cell(r, c).value for c in range(1, 8)]}")

print(f"\nTotal rows with nominal in Tabel_Mutasi: {len(active_rows)}")
non_zero_rows = [x for x in active_rows if abs(x[4]) > 0.001]
print(f"Non-zero active rows: {len(non_zero_rows)}")
for nr in non_zero_rows[:5]:
    print(f"  R{nr[0]:2d}: No={nr[1]} Tgl={nr[2]} Jam={nr[3]} Nom={nr[4]:>12,.2f} Tipe={nr[5]} Saldo={nr[6]:>12,.2f}")
print("  ...")
for nr in non_zero_rows[-5:]:
    print(f"  R{nr[0]:2d}: No={nr[1]} Tgl={nr[2]} Jam={nr[3]} Nom={nr[4]:>12,.2f} Tipe={nr[5]} Saldo={nr[6]:>12,.2f}")
