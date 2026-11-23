import sys
sys.path.insert(0, 'src')
import bank_mandiri_spec
for attr in dir(bank_mandiri_spec):
    if not attr.startswith('_'):
        print(f"{attr} = {getattr(bank_mandiri_spec, attr)}")
