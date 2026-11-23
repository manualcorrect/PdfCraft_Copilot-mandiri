import re
import zlib

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

for m in re.finditer(rb'(\d+)\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL):
    oid = int(m.group(1))
    try:
        decomp = zlib.decompress(m.group(3))
        # Find any Tj or TJ
        text_cmds = re.findall(rb'(\(.*?\)|<[0-9a-fA-F]+>)\s*(Tj|TJ)', decomp)
        # Look for "of" or "dari" or page numbers or numbers
        sample = []
        for tc, op in text_cmds:
            if b"006F0066" in tc or b"of" in tc or b"dari" in tc or b"10" in tc or b"00310030" in tc:
                sample.append((tc, op))
        if sample:
            print(f"Obj {oid} has matches:", sample)
    except Exception as e:
        pass
