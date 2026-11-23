import sys, os
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
import openpyxl, pdfplumber, re

excel_path = r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output\Template_Mutasi_AUG_OUTPUT_1.xlsx"
wb = openpyxl.load_workbook(excel_path, data_only=True)
ws = wb['Tabel_Mutasi']

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf"

# Extract orig saldos
pdf_tx_meta = []
with pdfplumber.open(pdf_path) as pdf:
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

fp = open(pdf_path, "rb")
parser = PDFParser(fp)
doc = PDFDocument(parser)

pages_data = []
for page in PDFPage.create_pages(doc):
    raw = b"".join(c.get_data() for c in page.contents)
    pages_data.append(raw)

def to_utf16_be(text):
    return text.encode('utf-16-be')

print("Checking old saldos in raw page streams:")
for tx_idx in range(33, 58):
    p_num = pdf_tx_meta[tx_idx]['page']
    old_sal_str = pdf_tx_meta[tx_idx]['orig_sal_str']
    new_sal_val = float(ws.cell(6 + tx_idx, 7).value) + 0.81
    new_sal_str = f"{new_sal_val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    old_bytes = to_utf16_be(old_sal_str)
    raw = pages_data[p_num - 1]
    found = old_bytes in raw
    print(f"Tx {tx_idx+1:2d} (Page {p_num}): old='{old_sal_str}' in raw? {found} -> new='{new_sal_str}'")
