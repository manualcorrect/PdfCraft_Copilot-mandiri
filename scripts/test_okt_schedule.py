import datetime
import re
import pdfplumber

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\okt\0.pdf"

pdf_tx_meta = []
with pdfplumber.open(pdf_path) as pdf:
    for p_idx, page in enumerate(pdf.pages):
        words = page.extract_words()
        min_top = 320 if p_idx == 0 else 200
        table_words = [w for w in words if min_top <= w['top'] <= 800]
        wibs = sorted([w for w in table_words if w['text'] == 'WIB'], key=lambda x: x['top'])
        for w in wibs:
            t_candidates = [x for x in table_words if abs(x['top'] - w['top']) < 3 and x['x1'] <= w['x0'] + 1]
            time_str = f"{t_candidates[-1]['text']} WIB" if t_candidates else '12:00:00 WIB'
            d_candidates = [x for x in table_words if 0 < (w['top'] - x['top']) < 15 and 45 <= x['x0'] <= 95]
            d_candidates.sort(key=lambda x: x['x0'])
            d_str = " ".join([x['text'] for x in d_candidates])
            m = re.search(r'^(\d+)', d_str)
            day_num = int(m.group(1)) if m else 1
            pdf_tx_meta.append({
                'orig_day': day_num,
                'orig_time': time_str,
                'orig_date': d_str
            })

assert len(pdf_tx_meta) == 70

sal_idx = 52 # Tx 53 (0-based 52)
schedule = [None] * 70

# Pre-salary groups (Tx 1..52, indices 0..51)
pre_groups = []
seen = {}
for i in range(sal_idx):
    key = (pdf_tx_meta[i]['orig_day'], pdf_tx_meta[i]['orig_time'])
    if key not in seen:
        seen[key] = len(pre_groups)
        pre_groups.append({
            'key': key,
            'indices': [i],
            'day': pdf_tx_meta[i]['orig_day'],
            'time': pdf_tx_meta[i]['orig_time']
        })
    else:
        pre_groups[seen[key]]['indices'].append(i)

print(f"Pre-salary groups: {len(pre_groups)}")
start_pre = datetime.datetime(2026, 10, 1, 9, 0, 0)
end_pre = datetime.datetime(2026, 10, 24, 18, 0, 0)
pre_span = (end_pre - start_pre).total_seconds()
step_pre = pre_span / max(1, len(pre_groups))

prev_dt = start_pre
for g_idx, g in enumerate(pre_groups):
    cur_dt = start_pre + datetime.timedelta(seconds=g_idx * step_pre + ((g_idx * 137) % 720))
    if cur_dt.hour < 8:
        cur_dt = cur_dt.replace(hour=8, minute=20 + (g_idx * 3 % 35))
    elif cur_dt.hour >= 23:
        cur_dt = cur_dt.replace(hour=21, minute=15 + (g_idx * 5 % 30))
    if cur_dt <= prev_dt:
        cur_dt = prev_dt + datetime.timedelta(minutes=2, seconds=30)
    prev_dt = cur_dt
    
    d_str = f"{cur_dt.day:02d} Oct 2026"
    t_str = f"{cur_dt.strftime('%H:%M:%S')} WIB"
    for idx in g['indices']:
        schedule[idx] = {'date': d_str, 'time': t_str, 'dt': cur_dt}

# Salary Tx 53
schedule[sal_idx] = {
    'date': '25 Oct 2026',
    'time': '04:00:00 WIB',
    'dt': datetime.datetime(2026, 10, 25, 4, 0, 0)
}

# Closing Fee Tx 70
schedule[69] = {
    'date': '31 Oct 2026',
    'time': '23:59:00 WIB',
    'dt': datetime.datetime(2026, 10, 31, 23, 59, 0)
}

# Post-salary intermediate groups (Tx 54..69, indices 53..68)
post_groups = []
p_seen = {}
for i in range(sal_idx + 1, 69):
    key = (pdf_tx_meta[i]['orig_day'], pdf_tx_meta[i]['orig_time'])
    if key not in p_seen:
        p_seen[key] = len(post_groups)
        post_groups.append({'indices': [i], 'key': key})
    else:
        post_groups[p_seen[key]]['indices'].append(i)

print(f"Post-salary groups: {len(post_groups)}")
start_post = datetime.datetime(2026, 10, 25, 11, 30, 0)
end_post = datetime.datetime(2026, 10, 31, 20, 0, 0)
post_span = (end_post - start_post).total_seconds()
step_post = post_span / max(1, len(post_groups))

prev_post = start_post
for g_i, g in enumerate(post_groups):
    cur_dt = start_post + datetime.timedelta(seconds=g_i * step_post + ((g_i * 113) % 600))
    if cur_dt.hour < 8:
        cur_dt = cur_dt.replace(hour=8, minute=20 + (g_i * 3 % 35))
    elif cur_dt.hour >= 23:
        cur_dt = cur_dt.replace(hour=21, minute=15 + (g_i * 5 % 30))
    if cur_dt <= prev_post:
        cur_dt = prev_post + datetime.timedelta(minutes=3, seconds=15)
    prev_post = cur_dt
    
    d_str = f"{cur_dt.day:02d} Oct 2026"
    t_str = f"{cur_dt.strftime('%H:%M:%S')} WIB"
    for idx in g['indices']:
        schedule[idx] = {'date': d_str, 'time': t_str, 'dt': cur_dt}

# Verify schedule
print("\nVerifying Schedule:")
for i in range(70):
    item = schedule[i]
    assert item is not None, f"Tx #{i+1} is None"
    if i > 0:
        prev = schedule[i-1]
        assert item['dt'] >= prev['dt'], f"Chronology error at Tx #{i+1}: {item['dt']} < {prev['dt']}"
    if i in [0, 1, 51, 52, 53, 68, 69]:
        print(f"Tx #{i+1:02d}: {item['date']} | {item['time']}")

print("All 70 transactions verified perfectly non-decreasing!")
