# KATALOG PENGUJIAN & PROSEDUR VERIFIKASI
## Engine: PdfCraft Copilot

Dokumen ini mendokumentasikan seluruh rangkaian pengujian unit, pengujian integrasi, audit forensik bounding box, serta verifikasi matematis yang tersedia di repositori **PdfCraft_Copilot**.

---

## 1. Kategori Pengujian Dokumen

Pengujian dalam repositori ini terbagi menjadi 4 lapisan kualitas (*Quality Assurance Layers*):

```
┌────────────────────────────────────────────────────────┐
│  Layer 4: Visual Forensic Audit (PNG Crop & Compare)   │
├────────────────────────────────────────────────────────┤
│  Layer 3: Bounding Box & Ruler Guides Audit (pdfplumber)│
├────────────────────────────────────────────────────────┤
│  Layer 2: Mathematical Balance Audit (OpenPyXL / Math) │
├────────────────────────────────────────────────────────┤
│  Layer 1: Syntax & Layout Engine Unit Tests            │
└────────────────────────────────────────────────────────┘
```

---

## 2. Katalog Script Verifikasi Utama (`scripts/`)

| Nama Script | Dokumen Target | Aspek yang Diuji |
| :--- | :--- | :--- |
| `scripts/verify_wafiq_okt_final.py` | `REK_WAFIQ_OKT_OUTPUT_PERFECT.pdf` | Audit 69 parameter: neraca klop 100%, salary 4 baris, penutup bulan 1 baris baseline, font purity TTInterphases. |
| `scripts/verify_wafiq_sep_final.py` | `REK_WAFIQ_SEP_OUTPUT_PERFECT.pdf` | Audit neraca klop, kesinambungan saldo berjalan (,81), stream replacement tanpa decompress truncated. |
| `scripts/verify_wafiq_aug_final.py` | `REK_WAFIQ_AUG_OUTPUT_PERFECT.pdf` | Audit 57 parameter: Tx 33 tarik tunai ATM, Tx 34 biaya admin, salary simetris 4 baris. |
| `scripts/verify_ibnu_okt_final.py` | `REK_IBNU_OKT_OUTPUT_1.pdf` | Alignment kotak ringkasan, right-edge nominal/saldo, audit seluruh 7 halaman, verifikasi rekonsiliasi neraca. |
| `scripts/verify_ibnu_sep_final.py` | `REK_IBNU_SEP_OUTPUT_1.pdf` | Keselarasan halaman ganjil-genap, stream UTF-16BE replacement, kontinuitas saldo dari bulan Agustus. |
| `scripts/verify_ibnu_aug_final.py` | `REK_IBNU_AUG_OUTPUT_1.pdf` | Pengujian baseline baris pertama, format tanggal ganda, dan kelengkapan footer regulasi. |
| `scripts/verify_keisya_aug.py` | `REK_KEISYA_AUG_OUTPUT_1.pdf` | Validasi subset font `TTInterphases`, koordinat kolom $No$, $Tanggal$, $Keterangan$, $Nominal$, $Saldo$. |
| `scripts/verify_sep_perfect.py` | `REK_GALANG_SEP_2026_PERFECT.pdf` | Pengujian rekonsiliasi saldo berjalan antar baris transaksi berulang. |
| `scripts/verify_okt_font_objs.py` | Seluruh Halaman Oktober | Memastikan tidak ada font default (Helvetica/Times) yang bocor ke dalam dokumen. |

---

## 3. Prosedur Audit Bounding Box Spasial (`pdfplumber`)

Setiap script verifikasi memanfaatkan `pdfplumber` untuk mengekstrak kata dan bounding box dengan toleransi $\pm 0.5\text{ pt}$.

### Parameter Toleransi Baku:
1. **Titik Dua (Colons `:`)**:
   * Header Informasi: $X \in [110.5, 111.5]\text{ pt}$ dan $X \in [325.5, 326.5]\text{ pt}$.
   * Kotak Ringkasan Finansial: Mengunci tegak lurus di $X = 446.12\text{ pt}$.
2. **Right-Edge Alignment (Batas Kanan Mutlak)**:
   * Seluruh angka nominal: $\max(x_1) \le 432.00\text{ pt}$.
   * Seluruh angka saldo: $\max(x_1) \le 571.00\text{ pt}$.
   * Nilai pada kotak ringkasan: $\max(x_1) \le 567.00\text{ pt}$.
3. **Penyusunan Keterangan**:
   * Seluruh baris dimulai dari $X = 124.00\text{ pt}$.
   * Lebar maksimal teks tidak boleh melebihi $X = 364.00\text{ pt}$ ($240.00\text{ pt}$ span).

---

## 4. Prosedur Audit Matematis (Reconciliation Check)

Persamaan neraca wajib bernilai identik pada setiap baris:
$$\text{Saldo}_i = \text{Saldo}_{i-1} + \text{Nominal}_i$$
Dan untuk keseluruhan periode:
$$\text{Saldo Akhir} = \text{Saldo Awal} + \text{Total Dana Masuk} - \text{Total Dana Keluar}$$

Contoh output audit sukses dari `verify_ibnu_okt_final.py`:
```text
=================================================================
COMPREHENSIVE AUDIT REPORT: IBNU AGUN - OKTOBER 2026
=================================================================
--- 1. SUMMARY BOX GEOMETRY & ALIGNMENT AUDIT (PAGE 1) ---
Top 168.92 pt | X: [298.00 .. 567.00] | Content: Saldo Awal/Initial Balance : 8.742.150,00
Top 191.92 pt | X: [298.00 .. 567.00] | Content: Dana Masuk/Incoming Transactions : + 45.100.000,00
Top 214.92 pt | X: [298.00 .. 567.00] | Content: Dana Keluar/Outgoing Transactions : - 48.243.000,00
Top 238.92 pt | X: [298.00 .. 567.00] | Content: Saldo Akhir/Closing Balance : 5.599.150,00
Balance Check: 8742150.0 + 45100000.0 - 48243000.0 = 5599150.0 (MATCH: EXACT)
STATUS: 100% AUDIT PASS
```

---

## 5. Menjalankan Verifikasi Cepat

Untuk memverifikasi statement yang baru dihasilkan:
```bash
# Menjalankan audit geometri dan angka
python scripts/verify_ibnu_okt_final.py

# Menjalankan benchmark regresi sintaks
python description_training_system/trainer_evaluator.py
```
Jika tidak ada error atau warning yang dimunculkan, dokumen telah memenuhi standar baku perbankan.
