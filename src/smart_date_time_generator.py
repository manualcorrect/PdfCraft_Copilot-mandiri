import re
import calendar
from datetime import datetime, timedelta

MONTHS_MAP = {
    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'mei': 5, 'may': 5,
    'jun': 6, 'jul': 7, 'agu': 8, 'agt': 8, 'aug': 8, 'sep': 9,
    'okt': 10, 'oct': 10, 'nov': 11, 'des': 12, 'dec': 12
}

MONTHS_INV = {
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
}

def parse_period_range(p_str):
    m = re.findall(r'(\d{1,2})\s+([A-Za-z]{3})\s+(\d{4})', str(p_str or ""))
    if len(m) >= 2:
        d1, m1, y1 = m[0]
        d2, m2, y2 = m[1]
        dt1 = datetime(int(y1), MONTHS_MAP.get(m1.lower(), 1), int(d1))
        dt2 = datetime(int(y2), MONTHS_MAP.get(m2.lower(), 1), int(d2))
        return dt1, dt2
    now = datetime.now()
    return datetime(now.year, now.month, 1), datetime(now.year, now.month, 28)

def shuffle_and_synchronize_schedule(transactions, month_num, year=2026, salary_no=22, last_day=None):
    """
    Applies synchronized shuffling pre-salary and chronological distribution post-salary.
    1. Pre-salary: Subtle jitter/shift, with 100% synchronous timestamps for clustered/repeated txs.
    2. Salary: Fixed at 25th of month 04:00:00 WIB.
    3. Post-salary: Distributed chronologically until last day of month.
    4. Month-end admin fee: Fixed at last day 23:59:00 WIB.
    """
    if not transactions:
        return transactions

    if last_day is None:
        last_day = calendar.monthrange(year, month_num)[1]

    m_str = MONTHS_INV.get(month_num, 'Sep')

    # Find salary index
    sal_idx = None
    for i, tx in enumerate(transactions):
        t_no = str(tx.get('no', '')).strip()
        u_str = str(tx.get('desc', '')).upper()
        if t_no == str(salary_no) or 'BENDI NASHA' in u_str or 'GAJI' in u_str:
            sal_idx = i
            break
    if sal_idx is None:
        sal_idx = min(len(transactions) - 1, 21)

    result_txs = [dict(tx) for tx in transactions]

    # -------------------------------------------------------------
    # 1. PRE-SALARY TRANSACTIONS (0 to sal_idx - 1)
    # -------------------------------------------------------------
    pre_groups = []
    seen = {}
    for i in range(sal_idx):
        tx = transactions[i]
        key = (str(tx.get('date', '')).strip(), str(tx.get('time', '')).strip())
        if key not in seen:
            seen[key] = len(pre_groups)
            pre_groups.append({
                'orig_key': key,
                'indices': [i],
                'orig_date': tx.get('date', ''),
                'orig_time': tx.get('time', '')
            })
        else:
            pre_groups[seen[key]]['indices'].append(i)

    salary_dt = datetime(year, month_num, 25, 4, 0, 0)
    
    # Parse original group datetimes
    group_dts = []
    for g in pre_groups:
        d_raw = str(g['orig_date'])
        t_raw = str(g['orig_time']).replace(' WIB', '').strip()
        m = re.search(r'(\d+)', d_raw)
        day = int(m.group(1)) if m else 1
        t_parts = [int(p) for p in t_raw.split(':')] if ':' in t_raw else [12, 0, 0]
        while len(t_parts) < 3:
            t_parts.append(0)
        dt = datetime(year, month_num, min(day, 24), min(t_parts[0], 23), min(t_parts[1], 59), min(t_parts[2], 59))
        group_dts.append(dt)

    # Shift each group slightly while preserving strict non-decreasing order
    shifted_dts = []
    prev_dt = datetime(year, month_num, 1, 0, 0, 0)
    for idx, dt in enumerate(group_dts):
        jitter_mins = 2 + (idx * 3) % 8
        jitter_secs = (idx * 13) % 55
        new_dt = dt + timedelta(minutes=jitter_mins, seconds=jitter_secs)
        if new_dt <= prev_dt:
            new_dt = prev_dt + timedelta(minutes=1, seconds=20)
        if new_dt >= salary_dt:
            new_dt = salary_dt - timedelta(hours=1, minutes=(len(group_dts) - idx) * 15)
        shifted_dts.append(new_dt)
        prev_dt = new_dt

    # Assign shifted timestamps to result
    for g_idx, g in enumerate(pre_groups):
        dt = shifted_dts[g_idx]
        d_str = f"{dt.day:02d} {m_str} {year}"
        t_str = f"{dt.strftime('%H:%M:%S')} WIB"
        for i in g['indices']:
            result_txs[i]['date'] = d_str
            result_txs[i]['time'] = t_str

    # -------------------------------------------------------------
    # 2. SALARY TRANSACTION (sal_idx)
    # -------------------------------------------------------------
    result_txs[sal_idx]['date'] = f"25 {m_str} {year}"
    result_txs[sal_idx]['time'] = "04:00:00 WIB"

    # -------------------------------------------------------------
    # 3. POST-SALARY TRANSACTIONS (sal_idx + 1 to len - 1)
    # -------------------------------------------------------------
    post_indices = list(range(sal_idx + 1, len(transactions)))
    if post_indices:
        # Closing fee is the last transaction
        last_i = post_indices[-1]
        result_txs[last_i]['date'] = f"{last_day:02d} {m_str} {year}"
        result_txs[last_i]['time'] = "23:59:00 WIB"

        # Intermediate post-salary items
        inter_indices = post_indices[:-1]
        if inter_indices:
            post_groups = []
            p_seen = {}
            for i in inter_indices:
                tx = transactions[i]
                key = (str(tx.get('date', '')).strip(), str(tx.get('time', '')).strip())
                if key not in p_seen:
                    p_seen[key] = len(post_groups)
                    post_groups.append({'indices': [i], 'orig_key': key})
                else:
                    post_groups[p_seen[key]]['indices'].append(i)

            start_post_dt = datetime(year, month_num, 25, 9, 30, 0)
            end_post_dt = datetime(year, month_num, last_day, 19, 0, 0)
            total_sec = (end_post_dt - start_post_dt).total_seconds()
            step_sec = total_sec / max(1, len(post_groups))

            for g_i, g in enumerate(post_groups):
                cur_dt = start_post_dt + timedelta(seconds=g_i * step_sec + ((g_i * 179) % 1200))
                # Normalize nighttime into daytime business hours (08:00 - 22:30)
                if cur_dt.hour < 7:
                    cur_dt = cur_dt.replace(hour=8, minute=15 + (g_i * 7 % 35))
                elif cur_dt.hour >= 23:
                    cur_dt = cur_dt.replace(hour=21, minute=20 + (g_i * 5 % 30))

                d_str = f"{cur_dt.day:02d} {m_str} {year}"
                t_str = f"{cur_dt.strftime('%H:%M:%S')} WIB"
                for i in g['indices']:
                    result_txs[i]['date'] = d_str
                    result_txs[i]['time'] = t_str

    return result_txs
