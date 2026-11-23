import re

for label, p in [('SEP', 'output/REK_KEISYA_SEP_OUTPUT_1.pdf'), ('OKT', 'output/REK_KEISYA_OKT_OUTPUT_1.pdf')]:
    with open(p, 'rb') as f:
        data = f.read()
    sx = int(re.findall(rb'startxref[\r\n]+(\d+)', data)[-1])
    print(f"\n{label} startxref: {sx}")
    print(data[sx:sx+300])
