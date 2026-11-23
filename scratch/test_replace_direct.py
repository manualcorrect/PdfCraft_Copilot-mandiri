import zlib, shutil, re, pdfplumber

src = r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output\REK_KEISYA_AUG_OUTPUT_1.pdf"
dst = r"scratch/test_replaced_stream.pdf"

with open(src, "rb") as f:
    pdf_bytes = f.read()

# We need to replace all 25 old saldos from Tx 34 to Tx 58
# Let's map old saldo bytes -> new saldo bytes
import openpyxl

excel_path = r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output\Template_Mutasi_AUG_OUTPUT_1.xlsx"
wb = openpyxl.load_workbook(excel_path, data_only=True)
ws = wb['Tabel_Mutasi']

# Extract orig saldos from 0.pdf
pdf_tx_meta = []
with pdfplumber.open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf") as pdf:
    for p_idx in range(5):
        page = pdf.pages[p_idx]
        words = page.extract_words()
        min_top = 320 if p_idx == 0 else 200
        table_words = [w for w in words if min_top <= w['top'] <= 800]
        wibs = sorted([w for w in table_words if w['text'] == 'WIB'], key=lambda x: x['top'])
        for w in wibs:
            sal_c = [x for x in table_words if abs(x['top'] - w['top']) < 12 and 500 <= x['x0'] and x['x1'] <= 575]
            sal_str = sal_c[0]['text'] if sal_c else ""
            pdf_tx_meta.append({
                'page': p_idx + 1,
                'orig_sal_str': sal_str
            })

replacements = []
for tx_idx in range(33, 58):
    old_sal_str = pdf_tx_meta[tx_idx]['orig_sal_str']
    new_sal_val = float(ws.cell(6 + tx_idx, 7).value) + 0.81
    new_sal_str = f"{new_sal_val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    old_b = old_sal_str.encode('utf-16-be')
    new_b = new_sal_str.encode('utf-16-be')
    replacements.append((old_b, new_b, old_sal_str, new_sal_str, tx_idx+1))

print(f"Total replacements to perform: {len(replacements)}")

# Find and decompress streams in pdf_bytes
# Replace targets, recompress, and rebuild PDF
# In a PDF file, streams are marked by stream ... endstream
stream_pattern = re.compile(rb'(\d+\s+\d+\s+obj\s*<<.*?>>\s*stream[\r\n]+)(.*?)([\r\n]+endstream\s*endobj)', re.DOTALL)

def replacer(match):
    header = match.group(1)
    body = match.group(2)
    footer = match.group(3)
    try:
        decomp = zlib.decompress(body)
        modified = False
        for old_b, new_b, old_s, new_s, tx_no in replacements:
            if old_b in decomp:
                # Check for kerning adjustment if length differs (Tx 57 and Tx 58)
                if old_s == '979.988,81' and new_s == '2.703.988,81':
                    # -62620 -> -61765
                    decomp = decomp.replace(b"-62620", b"-61765")
                    decomp = decomp.replace(b"-62619", b"-61765")
                elif old_s == '679.988,81' and new_s == '2.698.988,81':
                    # -62620 -> -61765
                    decomp = decomp.replace(b"-62620", b"-61765")
                    decomp = decomp.replace(b"-62619", b"-61765")
                
                decomp = decomp.replace(old_b, new_b)
                print(f"Replaced Tx {tx_no}: {old_s} -> {new_s}")
                modified = True
        if modified:
            new_compressed = zlib.compress(decomp)
            # Update /Length in header
            new_header = re.sub(rb'/Length\s+\d+', f'/Length {len(new_compressed)}'.encode(), header)
            return new_header + new_compressed + footer
    except Exception as e:
        pass
    return match.group(0)

new_pdf_bytes = stream_pattern.sub(replacer, pdf_bytes)

with open(dst, "wb") as f:
    f.write(new_pdf_bytes)

print("Saved:", dst)

# Now verify with pdfplumber!
with pdfplumber.open(dst) as pdf:
    print("\n--- Verifying extracted saldos from dst ---")
    for tx_idx in range(33, 58):
        p_num = pdf_tx_meta[tx_idx]['page']
        page = pdf.pages[p_num - 1]
        words = page.extract_words()
        expected = f"{float(ws.cell(6 + tx_idx, 7).value) + 0.81:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        # check if expected is in words
        found = any(w['text'] == expected and w['x0'] > 500 for w in words)
        w_match = [w for w in words if w['text'] == expected and w['x0'] > 500]
        pos_str = f"x0={w_match[0]['x0']:.2f}, x1={w_match[0]['x1']:.2f}" if w_match else "NOT_FOUND"
        print(f"Tx {tx_idx+1:2d} (Page {p_num}): expected={expected} -> match={found} ({pos_str})")
