# PANDUAN OPERASIONAL & STANDAR PROSEDUR OPERASIONAL (SOP) PRODUKSI
## Engine: PdfCraft Copilot (Bank Mandiri e-Statement Generator)

Panduan ini mendokumentasikan seluruh prosedur baku untuk menjalankan, memproduksi, dan memvalidasi rekening koran (*e-Statement*) Bank Mandiri pada perangkat manapun menggunakan repositori **PdfCraft_Copilot**.

---

## 1. Persiapan Awal di Perangkat Baru

### A. Prasyarat Sistem
* **Python**: Versi `3.10` atau `3.11` (direkomendasikan).
* **Git**: Terpasang dan terkonfigurasi.
* **OS**: Windows, macOS, atau Linux.

### B. Langkah Kloning & Instalasi Dependensi
```bash
# 1. Kloning repositori
git clone https://github.com/manualcorrect/PdfCraft_Copilot-mandiri.git
cd PdfCraft_Copilot-mandiri

# 2. Buat dan aktifkan virtual environment (opsional namun disarankan)
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# 3. Instal dependensi library
pip install -r requirements.txt
```

---

## 2. Struktur Master Dokumen & Template

Repositori ini telah menyediakan template master yang siap digunakan di folder `templates/`:
1. `templates/master_page_1.pdf`: Halaman 1 baku (memuat banner header biru, info nasabah, dan kotak ringkasan saldo finansial).
2. `templates/master_page_intermediate.pdf`: Halaman perantara (halaman 2 s.d. $N-1$) dengan header tabel transaksi penuh (kapasitas 12 baris).
3. `templates/master_page_disclaimer_inline.pdf`: Halaman penutup mutasi yang memuat tabel transaksi (maksimal 7 baris) diikuti pembatas *"ini adalah batas akhir transaksi anda"*, klausul Disclaimer 4 poin, dan legalitas footer OJK/BI/LPS.
4. `templates/master_page_disclaimer_standalone.pdf`: Halaman penutup murni jika baris mutasi tepat menghabiskan halaman sebelumnya.
5. `templates/Template_Mutasi_Bank.xlsx` / `templates/Template_Mutasi_PdfCraft_Copilot.xlsx`: Template data mutasi Excel standar.

---

## 3. Alur Kerja Standar (SOP 7-Tahap Produksi)

```
[1. Input Excel Mutasi] ──► [2. Parse & Rekonsiliasi Neraca]
                                      │
                                      ▼
[4. Format Multi-line Keterangan] ◄── [3. Smart Scheduling Jam & Tanggal]
         │
         ▼
[5. Chunking & Master PDF Assembly]
         │
         ▼
[6. Low-Level Stream Patching (Font & Identity-H)]
         │
         ▼
[7. Automated Mathematical & Spatial Audit] ──► [PDF Final Lulus Audit]
```

### Tahap 1: Persiapan Input Data Transaksi (Excel)
Pastikan kolom Excel memuat:
* `No`: Nomor urut mutasi ($1 \dots N$).
* `Tanggal`: Format tanggal standar (contoh: `01/08/2026`).
* `Keterangan`: Deskripsi mentah transaksi (contoh: `Transfer BI Fast Dari BCA PT BENDI NASHA NIAGA INDUSTRI 5411078192 (CENAIDJA)`).
* `Nominal (IDR)`: Nilai transaksi (positif untuk kredit/masuk, negatif untuk debit/keluar).
* `Saldo (IDR)`: Saldo berjalan setelah transaksi.
* *Header Metadata*: Nama Nasabah, Nomor Rekening, Cabang, Periode, Saldo Awal.

### Tahap 2: Parsing & Verifikasi Neraca (`src/parse_excel_template.py`)
Modul ini membaca sheet transaksi dan melakukan auto-reconcile:
$$\text{Saldo Akhir} = \text{Saldo Awal} + \sum \text{Kredit} - \sum \text{Debit}$$
Jika terdapat selisih pembulatan, parser memberikan peringatan sebelum proses PDF dimulai.

### Tahap 3: Penjadwalan Waktu Realistis (`src/smart_date_time_generator.py`)
Menghasilkan stempel jam transaksi (`HH:MM:SS WIB`) yang realistis:
* Mengikuti jam operasional wajar (07:00 s.d. 21:00 WIB).
* Memastikan transaksi berurutan dalam hari yang sama memiliki selisih waktu logis ($\ge 1\text{ menit}$).
* Menghindari lonjakan transaksi payroll di luar jam perbankan.

### Tahap 4: Format Keterangan Otomatis (`src/description_layout_engine.py`)
* Mengklasifikasikan deskripsi ke dalam 9 kategori perbankan baku.
* Membagi teks panjang menjadi $1, 2, 3,$ atau $4$ baris tanpa melebihi batas lebar kolom ($240.00\text{ pt}$).
* Menghitung offset vertikal simetris terhadap baseline ($Y_{\text{base}}$):
  * **1 Baris**: $Y = Y_{\text{base}}$
  * **2 Baris**: $Y = Y_{\text{base}} \pm 5.00\text{ pt}$
  * **3 Baris**: $Y = Y_{\text{base}} - 10.00\text{ pt},\; Y_{\text{base}},\; Y_{\text{base}} + 10.00\text{ pt}$
  * **4 Baris**: $Y = Y_{\text{base}} - 15.00\text{ pt},\; Y_{\text{base}} - 5.00\text{ pt},\; Y_{\text{base}} + 5.00\text{ pt},\; Y_{\text{base}} + 15.00\text{ pt}$

### Tahap 5: Pembagian Halaman (*Chunking*) & Assembling PDF
* **Halaman 1**: Mengambil persis **10 transaksi pertama**.
* **Halaman 2 s.d. $N-1$**: Mengambil persis **12 transaksi per halaman**.
* **Halaman Terakhir**:
  * Jika sisa transaksi $\le 7$: Gunakan `master_page_disclaimer_inline.pdf`.
  * Jika sisa transaksi $8 \dots 12$: Gunakan `master_page_intermediate.pdf` lalu tambahkan `master_page_disclaimer_standalone.pdf`.

### Tahap 6: Eksekusi Injeksi Objek & Stream Patching
Untuk menjaga integritas subset font `TTInterphases` Identity-H:
* Nomor Halaman diperbarui menjadi format baku: `1 dari N` dan `1 of N`.
* Angka Saldo Awal, Dana Masuk, Dana Keluar, dan Saldo Akhir pada Kotak Ringkasan Halaman 1 dikunci dengan posisi rata kanan (*Right-Edge*) di **$X = 567.00\text{ pt}$**.
* Kolom Nominal dikunci rata kanan di **$X = 432.00\text{ pt}$**.
* Kolom Saldo dikunci rata kanan di **$X = 571.00\text{ pt}$**.
* Menggunakan teknik **Descending Paragraph Order** saat memodifikasi objek teks untuk mencegah pergeseran indeks (*index drift*).

### Tahap 7: Audit Otomatis & Validasi Mutlak
Jalankan script verifikasi untuk memvalidasi:
```bash
python scripts/verify_ibnu_okt_final.py
```
Pemeriksaan mencakup:
1. Keselarasan titik dua (`:`) pada sumbu $X$.
2. Batas kanan angka nominal dan saldo.
3. Ketiadaan tabrakan teks (*zero collision*).
4. Persamaan neraca keuangan 100% klop.

---

## 4. Perintah Cepat Produksi (Quick Commands)

* **Menjalankan Evaluasi Training Sintaks Keterangan**:
  ```bash
  python description_training_system/trainer_evaluator.py
  ```
* **Mengekstrak Corpus Tambahan dari PDF Asli**:
  ```bash
  python description_training_system/corpus_harvester.py
  ```
* **Membangun Statement Menggunakan Builder Modular**:
  ```bash
  python scripts/build_ibnu_okt_final.py
  ```
