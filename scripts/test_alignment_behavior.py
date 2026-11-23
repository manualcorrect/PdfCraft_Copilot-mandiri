import os
import sys

sys.path.insert(0, os.path.abspath('.'))
sys.stdout.reconfigure(encoding='utf-8')

from src.pdfcraft_client import PdfCraftClient
import pdfplumber

client = PdfCraftClient()
src_pdf = os.path.abspath('templates/master_page_1.pdf')
test_pdf = os.path.abspath('output/test_align.pdf')

doc_id = client.doc_open(src_pdf)

# Let's inspect P#44 (first saldo: 6.364.500,81)
# and P#46 (first nominal: -2.500,00)
# and P#35 (1 dari) and P#34 (18) and P#28 (1 of 18)
paras = client.get_paragraphs(doc_id, 1)

print("Before edits:")
for p in paras:
    if p['paragraph'] in [28, 34, 35, 44, 46]:
        print(f"P#{p['paragraph']}: rect={p['rect']} text={repr(p['text'])}")

# Let's change P#44 to "354.955,00"
# In template, P#44 rect is [522.16, 343.92, 571.0, 351.92] (width = 48.84)
# What is width of "354.955,00"? Let's edit with text="354.955,00" without dx first, save, and inspect with pdfplumber!
client.edit_text(doc_id, 1, paragraph=44, text="354.955,00")
# Edit P#46 to "-500.000,00"
client.edit_text(doc_id, 1, paragraph=46, text="-500.000,00")

# Edit page numbers
# P#35 is "1 dari", P#34 is "18"
# Let's see what happens if we set P#35 text="1 dari 3" with width=40.0
client.edit_text(doc_id, 1, paragraph=35, text="1 dari 3", width=40.0)
client.edit_text(doc_id, 1, paragraph=34, text="")
client.edit_text(doc_id, 1, paragraph=28, text="1 of 3", width=40.0)

client.doc_save(doc_id, test_pdf)
client.doc_close(doc_id)

with pdfplumber.open(test_pdf) as pdf:
    words = pdf.pages[0].extract_words()
    print("\nAfter edits in saved PDF:")
    for w in words:
        if any(k in w['text'] for k in ['354.955', '-500.000', 'dari', 'of', '3']):
            print(f"Word: {w['text']:15s} x0={w['x0']:6.2f} x1={w['x1']:6.2f} top={w['top']:6.2f}")
