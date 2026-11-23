import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:/Users/Wisnu/.gemini/antigravity/brain/8915d7e6-f8d3-49ef-a02e-6a76f5a152ad/.system_generated/steps/233/output.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

for p in data['paragraphs']:
    rect = [round(x, 1) for x in p['rect']]
    print(f"P#{p['paragraph']:3d} | rect={rect} | sz={p.get('size')} | fnt={p.get('font','?')[:20]} | txt={repr(p['text'])}")
