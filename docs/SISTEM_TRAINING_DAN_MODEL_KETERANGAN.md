# SISTEM TRAINING & MODEL LOGIKA KETERANGAN TRANSAKSI
## Modul: `description_training_system`

Dokumen ini menjelaskan rancangan, metodologi training, arsitektur inferensi, serta tolok ukur evaluasi dari modul kecerdasan buatan dan aturan sintaks pemformatan keterangan transaksi Bank Mandiri.

---

## 1. Latar Belakang & Masalah yang Diselesaikan

Pada dokumen asli Bank Mandiri, kolom keterangan (*Remarks*) berukuran terbatas (lebar maksimum $240.00\text{ pt}$). Jika teks terlalu panjang, sistem perbankan Mandiri memecah uraian tersebut ke dalam $2, 3,$ atau $4$ baris dengan aturan pemisahan suku kata (*line break*) dan tata letak vertikal yang sangat spesifik:
* Jarak antar baris (*leading*) persis $\Delta Y = 10.00\text{ pt}$.
* Seluruh kumpulan baris harus terpusat secara simetris terhadap baseline baris transaksi ($Y_{\text{base}}$).
* Format nama pengirim, nomor rekening, bank perantara, dan kode referensi (misal: `(CENAIDJA)`) harus mengikuti tata bahasa baku Bank Mandiri.

Jika pemecahan baris dilakukan secara acak atau naif, teks mutasi akan bertabrakan dengan baris atas/bawahnya (*line collision*) atau meluber keluar dari batas kanan nominal.

---

## 2. Arsitektur Modul

```
[PDF Dokumen Asli]
       │
       ▼
[corpus_harvester.py] ──► ground_truth_corpus.json (251 Sampel Terlabeli)
                                     │
                                     ▼
[syntax_rules.py]       ──► [trainer_evaluator.py] ◄── [description_model.py]
  (9 Kategori Formal)                │
                                     ▼
                         [Laporan Evaluasi & Log]
                         - LATEST_TRAINING_REPORT.md
                         - training_history.jsonl
```

### A. Dataset Ground Truth (`ground_truth_corpus.json`)
Dataset diekstraksi dari ribuan baris mutasi rekening koran resmi Bank Mandiri:
1. `Agu 2026_unlocked.pdf` (18 Halaman, Roy Darwin Rezerius, 209 Transaksi)
2. `Mei 2026_unlocked.pdf` (Roy Darwin Rezerius)
3. `e-Statement_XXXXXXXXX9210_01 Des 2024-31 Des 2024_unlocked.pdf` (6 Halaman, Muhammad Nasih)
4. `e-Statement_XXXXXXXXX9648_01 Apr 2026-30 Apr 2026_unlocked.pdf` (Suhanda)

Total sampel ground-truth terlabeli: **251 sampel transaksi unik**.

---

## 3. Taksonomi 9 Kategori Transaksi Mandiri

Aturan sintaks formal (`syntax_rules.py`) memetakan setiap deskripsi mentah ke dalam kategori spesifik:

| Kategori | Pola Kata Kunci / Ciri Khusus | Contoh Format Baku |
| :--- | :--- | :--- |
| `PAYROLL_CORPORATE` | Mengandung nama PT pemberi upah, `GAJI`, atau `UPAH` | Baris 1: `Transfer BI Fast`<br>Baris 2: `Dari BCA`<br>Baris 3: `PT BENDI NASHA NIAGA INDUSTRI 5411078192`<br>Baris 4: `(CENAIDJA)` |
| `BI_FAST` | Transfer antar bank via sistem BI Fast | Baris 1: `Transfer BI Fast`<br>Baris 2: `Ke BRI`<br>Baris 3: `NAMA PENERIMA 0123456789` |
| `MANDIRI_INHOUSE` | Pemindahbukuan sesama rekening Mandiri | Baris 1: `Transfer dari BANK MANDIRI`<br>Baris 2: `SIGIT BUDHI ARYONO 1550009926679` |
| `ATM_WITHDRAWAL` | Tarik tunai kartu atau tanpa kartu | Baris 1: `Penarikan tunai tanpa kartu`<br>Baris 2: `Di ATM SRG AM PURI ANGREK 0`<br>Baris 3: `089622130569` |
| `QRIS_PAYMENT` | Transaksi merchant via Livin' QR | Baris 1: `Pembayaran QR`<br>Baris 2: `ke Kantin Ka Rin`<br>Baris 3: `507016923183` |
| `ECOMMERCE` | Belanja online (Shopee, Tokopedia, TikTok, Blibli, Lazada) | Baris 1: `Shopee Indonesia`<br>Baris 2: `8800108962213056` |
| `EWALLET_BILLER` | Top-up dompet digital / tagihan (Dana, Gopay, OVO, e-money, PLN, Telkomsel) | Baris 1: `Top-up e-money`<br>Baris 2: `6032982817401134` |
| `BANK_FEES_ADMIN` | Biaya administrasi bulanan, materai, biaya BI Fast | Baris 1: `Biaya administrasi rekening` (Single-line) |
| `GENERAL_TRANSFER` | Transfer kliring umum atau transaksi lainnya | Disesuaikan dengan batas lebar $240.00\text{ pt}$ |

---

## 4. Model Inferensi Spasial (`description_model.py`)

Fungsi utama `DescriptionModelEngine.format(raw_text)` mengembalikan objek terstruktur:
```python
{
    "category": "PAYROLL_CORPORATE",
    "lines": [
        "Transfer BI Fast",
        "Dari BCA",
        "PT BENDI NASHA NIAGA INDUSTRI 5411078192",
        "(CENAIDJA)"
    ],
    "formatted_text": "Transfer BI Fast\nDari BCA\nPT BENDI NASHA NIAGA INDUSTRI 5411078192\n(CENAIDJA)",
    "line_count": 4,
    "target_top_offset": -15.0,  # Offset dY dari baseline baris
    "max_width": 240.00,
    "is_safe": True
}
```

Rumus penetapan offset vertikal ($dY$) dari garis dasar ($Y_{\text{base}}$):
* Jika $N = 1 \implies dY = 0.0\text{ pt}$
* Jika $N = 2 \implies dY = -5.0\text{ pt}$
* Jika $N = 3 \implies dY = -10.0\text{ pt}$
* Jika $N = 4 \implies dY = -15.0\text{ pt}$

---

## 5. Prosedur Evaluasi & Pengujian Regresi (`trainer_evaluator.py`)

Untuk memvalidasi akurasi model di perangkat baru:
```bash
python description_training_system/trainer_evaluator.py
```

### Hasil Benchmark:
1. **Akurasi Klasifikasi**: **96.41%** (242 dari 251 sampel terklasifikasi sempurna).
2. **Keamanan Spasial**: **100.0% Zero Collision** (tidak ada teks yang melebihi batas batas baris $46.00\text{ pt}$).
3. **Hasil Mandatory Regression Test Suite**:
   * `TC-01`: Corporate Payroll PT Bendi Nasha Niaga Industri $\rightarrow$ **PASS**
   * `TC-02`: BI Fast dengan berita cicil upah $\rightarrow$ **PASS**
   * `TC-03`: In-house transfer rekening 13 digit $\rightarrow$ **PASS**
   * `TC-04`: Penarikan tunai tanpa kartu di ATM $\rightarrow$ **PASS**
   * `TC-05`: Pembayaran QRIS merchant 3 baris $\rightarrow$ **PASS**
   * `TC-06`: Biaya administrasi 1 baris $\rightarrow$ **PASS**

Setiap kali script ini dijalankan, ringkasan otomatis dicatat ke file `training_logs/training_history.jsonl` dan diekspor ke `training_logs/LATEST_TRAINING_REPORT.md`.
