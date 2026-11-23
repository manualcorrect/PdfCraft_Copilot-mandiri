import pdfplumber

chars_found = set()
with pdfplumber.open(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf') as pdf:
    for page in pdf.pages:
        for c in page.chars:
            chars_found.add(c['text'])

target_name = "KEISYA AULIA"
missing_name = [c for c in target_name if c not in chars_found]
print("Target name:", target_name)
print("Missing glyphs in 0.pdf:", missing_name)

target_branch = "KCP Serang Ciceri"
missing_branch = [c for c in target_branch if c not in chars_found]
print("Target branch:", target_branch)
print("Missing glyphs for branch:", missing_branch)

target_period = "01 Aug 2026 - 31 Aug 2026"
missing_period = [c for c in target_period if c not in chars_found]
print("Target period:", target_period)
print("Missing glyphs for period:", missing_period)

target_issued = "12 Nov 2026"
missing_issued = [c for c in target_issued if c not in chars_found]
print("Target issued:", target_issued)
print("Missing glyphs for issued:", missing_issued)
