import sys, re, datetime, calendar
sys.path.insert(0, 'src')

month_code = "Aug"
month_num = 8
year = 2026
last_day = 31

import openpyxl, pdfplumber

excel_path = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\Template_Mutasi_AUG.xlsx'
pdf_path = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf'

wb = openpyxl.load_workbook(excel_path, data_only=True)
ws = wb['Tabel_Mutasi']
excel_noms = [float(ws.cell(r, 5).value) for r in range(6, 64)]

pdf_tx_meta = []
with pdfplumber.open(pdf_path) as pdf:
    for p_idx in range(5):
        page = pdf.pages[p_idx]
        words = page.extract_words()
        min_top = 320 if p_idx == 0 else 200
        table_words = [w for w in words if min_top <= w['top'] <= 800]
        wibs = sorted([w for w in table_words if w['text'] == 'WIB'], key=lambda x: x['top'])
        for w in wibs:
            t_candidates = [x for x in table_words if abs(x['top'] - w['top']) < 3 and x['x1'] <= w['x0'] + 1]
            time_str = f"{t_candidates[-1]['text']} WIB" if t_candidates else "12:00:00 WIB"
            d_candidates = [x for x in table_words if 0 < (w['top'] - x['top']) < 15 and 45 <= x['x0'] <= 95]
            d_candidates.sort(key=lambda x: x['x0'])
            raw_d = " ".join([x['text'] for x in d_candidates]).strip()
            m = re.search(r'^(\d+)', raw_d)
            day_num = int(m.group(1)) if m else 1
            pdf_tx_meta.append({
                'orig_day': day_num,
                'orig_time': time_str,
                'orig_date': raw_d
            })

sal_idx = 33 # 0-based index for Tx 34 (salary)

schedule = [None] * 58

# 1. PRE-SALARY (0 to 32)
# Group by (orig_day, orig_time)
pre_groups = []
seen = {}
for i in range(sal_idx):
    key = (pdf_tx_meta[i]['orig_day'], pdf_tx_meta[i]['orig_time'])
    if key not in seen:
        seen[key] = len(pre_groups)
        pre_groups.append({'key': key, 'indices': [i], 'day': pdf_tx_meta[i]['orig_day'], 'time': pdf_tx_meta[i]['orig_time']})
    else:
        pre_groups[seen[key]]['indices'].append(i)

# Apply subtle shift (jitter by 2-5 minutes) while keeping non-decreasing order
prev_dt = datetime.datetime(year, month_num, 1, 0, 0, 0)
for g_idx, g in enumerate(pre_groups):
    t_clean = g['time'].replace(' WIB', '').strip()
    h, m, s = [int(p) for p in t_clean.split(':')]
    jitter_mins = (g_idx * 3 + 2) % 7
    jitter_secs = (g_idx * 17) % 55
    dt = datetime.datetime(year, month_num, g['day'], h, m, s) + datetime.timedelta(minutes=jitter_mins, seconds=jitter_secs)
    if dt <= prev_dt:
        dt = prev_dt + datetime.timedelta(minutes=1, seconds=15)
    prev_dt = dt
    
    d_str = f"{dt.day:02d} Aug {year}"
    t_str = f"{dt.strftime('%H:%M:%S')} WIB"
    for idx in g['indices']:
        schedule[idx] = {'date': d_str, 'time': t_str}

# 2. SALARY (Tx 34)
schedule[sal_idx] = {'date': '25 Aug 2026', 'time': '04:00:00 WIB'}

# 3. POST-SALARY (Tx 35 to 58, indices 34 to 57)
schedule[57] = {'date': '31 Aug 2026', 'time': '23:59:00 WIB'}

post_groups = []
p_seen = {}
for i in range(sal_idx + 1, 57):
    t_str = pdf_tx_meta[i]['orig_time']
    d_orig = pdf_tx_meta[i]['orig_day']
    key = (d_orig, t_str)
    if key not in p_seen:
        p_seen[key] = len(post_groups)
        post_groups.append({'indices': [i], 'key': key})
    else:
        post_groups[p_seen[key]]['indices'].append(i)

num_groups = len(post_groups)
start_dt = datetime.datetime(year, month_num, 25, 10, 30, 0)
end_dt = datetime.datetime(year, month_num, 30, 20, 0, 0)
total_sec = (end_dt - start_dt).total_seconds()
step_sec = total_sec / max(1, num_groups)

prev_post_dt = start_dt
for g_i, g in enumerate(post_groups):
    cur_dt = start_dt + datetime.timedelta(seconds=g_i * step_sec + ((g_i * 131) % 900))
    if cur_dt.hour < 8:
        cur_dt = cur_dt.replace(hour=8, minute=20 + (g_i * 3 % 35))
    elif cur_dt.hour >= 23:
        cur_dt = cur_dt.replace(hour=21, minute=15 + (g_i * 5 % 30))
    if cur_dt <= prev_post_dt:
        cur_dt = prev_post_dt + datetime.timedelta(minutes=2, seconds=45)
    prev_post_dt = cur_dt
    
    d_str = f"{cur_dt.day:02d} Aug {year}"
    t_str = f"{cur_dt.strftime('%H:%M:%S')} WIB"
    for idx in g['indices']:
        schedule[idx] = {'date': d_str, 'time': t_str}

print("=== GENERATED SCHEDULE FOR KEISYA AUGUST ===")
for i in range(len(schedule)):
    print(f"Tx {i+1:2d}: {schedule[i]['date']} | {schedule[i]['time']} | Nom={excel_noms[i]:>12,.2f}")
