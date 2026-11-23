# Laporan Monitoring Sistem Logika Training Keterangan
**Waktu Eksekusi:** `2026-11-02T22:28:24.108008`  
**Dataset Ground Truth:** `251 Sampel Transaksi Resmi Bank Mandiri`

---

## 1. Ringkasan Metrik Akurasi & Keamanan Spasial

| Metrik Evaluasi | Hasil Model | Target Baku | Status |
| :--- | :---: | :---: | :---: |
| **Akurasi Klasifikasi Kategori** | **96.41%** | $\ge 95.0\%$ | ✅ PASS |
| **Akurasi Pemisahan Baris (Line Count)** | **87.65%** | $\ge 95.0\%$ | ⚠️ REVIEW |
| **Kepatuhan Keamanan Spasial (Zero-Collision)** | **100.0%** | $100.0\%$ | ✅ PASS |
| **Hasil Uji Kasus Khusus (Edge Cases)** | **6 / 6** | $100\%$ | ✅ SEMUA LULUS |

---

## 2. Performa Berdasarkan Kategori Transaksi

| Kategori Transaksi | Total Sampel | Akurasi Kategori | Akurasi Format Baris |
| :--- | :---: | :---: | :---: |
| `ATM_WITHDRAWAL` | 23 | 100.0% | 100.0% |
| `BANK_FEES_ADMIN` | 7 | 85.7% | 57.1% |
| `BI_FAST` | 41 | 100.0% | 75.6% |
| `ECOMMERCE` | 2 | 100.0% | 50.0% |
| `EWALLET_BILLER` | 24 | 87.5% | 58.3% |
| `GENERAL_TRANSFER` | 25 | 80.0% | 80.0% |
| `MANDIRI_INHOUSE` | 7 | 100.0% | 71.4% |
| `PAYROLL_CORPORATE` | 6 | 100.0% | 100.0% |
| `QRIS_PAYMENT` | 116 | 100.0% | 100.0% |

---

## 3. Hasil Pengujian Kasus Khusus (Mandatory Regression Tests)

### TC-01-TX18-PAYROLL: Galang Jul Tx 18 / Salman Apr Row 14 Corporate Payroll [✅ PASS]
- **Kategori Prediksi:** `PAYROLL_CORPORATE` (Target: `PAYROLL_CORPORATE`)
- **Offset Vertikal ($dY$):** `-15.0 pt` dari garis dasar baris
- **Penyusunan Baris Prediksi:**
  1. `Transfer BI Fast`
  2. `Dari BCA`
  3. `PT BENDI NASHA NIAGA INDUSTRI 5411078192`
  4. `(CENAIDJA)`

### TC-02-BIFAST-FLAT: Single-line BI Fast with Bank and Remark [✅ PASS]
- **Kategori Prediksi:** `PAYROLL_CORPORATE` (Target: `PAYROLL_CORPORATE`)
- **Offset Vertikal ($dY$):** `-15.0 pt` dari garis dasar baris
- **Penyusunan Baris Prediksi:**
  1. `Transfer BI Fast`
  2. `Dari BCA`
  3. `KARINA AMALIA DARMAW 2452998221`
  4. `CICIL UPAH MEI 2026`

### TC-03-MANDIRI-INHOUSE: In-house Mandiri Transfer with Account Number [✅ PASS]
- **Kategori Prediksi:** `MANDIRI_INHOUSE` (Target: `MANDIRI_INHOUSE`)
- **Offset Vertikal ($dY$):** `-5.0 pt` dari garis dasar baris
- **Penyusunan Baris Prediksi:**
  1. `Transfer dari BANK MANDIRI`
  2. `SIGIT BUDHI ARYONO 1550009926679`

### TC-04-ATM-CARDLESS: Cardless ATM Cash Withdrawal (3 lines) [✅ PASS]
- **Kategori Prediksi:** `ATM_WITHDRAWAL` (Target: `ATM_WITHDRAWAL`)
- **Offset Vertikal ($dY$):** `-10.0 pt` dari garis dasar baris
- **Penyusunan Baris Prediksi:**
  1. `Penarikan tunai tanpa kartu`
  2. `Di ATM SRG AM PURI ANGREK 0`
  3. `089622130569`

### TC-05-QR-PAYMENT: QRIS Merchant Payment (3 lines) [✅ PASS]
- **Kategori Prediksi:** `QRIS_PAYMENT` (Target: `QRIS_PAYMENT`)
- **Offset Vertikal ($dY$):** `-10.0 pt` dari garis dasar baris
- **Penyusunan Baris Prediksi:**
  1. `Pembayaran QR`
  2. `ke Kantin Ka Rin`
  3. `507016923183`

### TC-06-BANK-FEE: Single-line Bank Fee [✅ PASS]
- **Kategori Prediksi:** `BANK_FEES_ADMIN` (Target: `BANK_FEES_ADMIN`)
- **Offset Vertikal ($dY$):** `0.0 pt` dari garis dasar baris
- **Penyusunan Baris Prediksi:**
  1. `Biaya administrasi rekening`

---
*Laporan ini dihasilkan secara otomatis oleh `DescriptionTrainerEvaluator` dan tersimpan secara permanen pada log monitoring.*
