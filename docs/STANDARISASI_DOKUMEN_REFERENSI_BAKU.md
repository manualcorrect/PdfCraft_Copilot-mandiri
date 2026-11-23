# STANDARISASI DOKUMEN REFERENSI BAKU: E-STATEMENT BANK MANDIRI
## Engine: PdfCraft Copilot Architecture
**Status:** Permanent Standard Reference (Baku)  
**Dokumen Referensi Asli:**
1. [Agu 2026_unlocked.pdf](file:///D:/X_Files/rekening/Reference/Roy/ilovepdf_unlocked/Agu%202026_unlocked.pdf) (18 Halaman, Roy Darwin Rezerius, 209 Transaksi)
2. [e-Statement_XXXXXXXXX9210_01 Des 2024-31 Des 2024_unlocked.pdf](file:///D:/X_Files/rekening/Reference/nasih%202024%20new%20unlocked/ilovepdf_unlocked/e-Statement_XXXXXXXXX9210_01%20Des%202024-31%20Des%202024_unlocked.pdf) (6 Halaman, Muhammad Nasih, 60 Transaksi)

---

## 1. SPESIFIKASI FISIK & KANVAS DOKUMEN
* **Format Kertas**: ISO A4 Portrait
* **Dimensi**: Lebar $595.00\text{ pt}$ ($20.99\text{ cm}$) $\times$ Tinggi $842.00\text{ pt}$ ($29.70\text{ cm}$)
* **Margin Acuan Utama**:
  * Margin Kiri Teks / Header: $X = 16.00\text{ pt}$
  * Margin Kiri Tabel (Kolom No): $X = 20.00\text{ pt}$
  * Margin Kanan Tabel (Batas Kanan Saldo): $X = 571.00\text{ pt}$
  * Margin Kanan Ringkasan Header: $X = 567.00\text{ pt}$
  * Margin Kanan Banner Header: $X = 579.00\text{ pt}$

---

## 2. STANDAR TIPOGRAFI & ENCODING FONT
Dokumen resmi perbankan menggunakan keluarga font **TTInterphases** (TrueType / OpenType Type0 Identity-H embedded):
1. **`TTInterphases-Bold`**:
   - Judul `e-Statement` ($16.0\text{ pt}$)
   - Judul Tipe Rekening, misal `Tabungan NOW IDR` ($12.0\text{ pt}$)
   - Judul `Disclaimer` ($12.0\text{ pt}$)
   - Label Header: `Nama/`, `Cabang/`, `Periode/`, `Dicetak pada/`, `Nomor Rekening/`, `Mata Uang/` ($8.0\text{ pt}$)
   - Header Ringkasan: `Saldo Awal/`, `Dana Masuk/`, `Dana Keluar/`, `Saldo Akhir/` ($8.0\text{ pt}$)
   - Angka Keuangan: Nominal Transaksi, Saldo Akhir Berjalan, Angka Ringkasan ($8.0\text{ pt}$)
   - Header Tabel Bahasa Indonesia: `No`, `Tanggal`, `Keterangan`, `Nominal (IDR)`, `Saldo (IDR)` ($8.0\text{ pt}$)
   - Nomor Halaman Bahasa Indonesia: `1 dari 18` ($8.0\text{ pt}$)
2. **`TTInterphases-Regular`**:
   - Alamat Bank Header ($8.0\text{ pt}$)
   - Isi Data Nasabah: Nama Nasabah, Nama Cabang, Rentang Periode, Tanggal Cetak, Nomor Rekening ($8.0\text{ pt}$)
   - Detail Mutasi: Tanggal Transaksi, Jam Transaksi (`HH:MM:SS WIB`), Seluruh baris Keterangan ($8.0\text{ pt}$)
   - Isi Klausul Disclaimer Bahasa Indonesia ($8.0\text{ pt}$)
   - Legal Footer Mandiri Call 14000 & OJK/BI/LPS ($8.0\text{ pt}$)
3. **`TTInterphases-Italic`**:
   - Label Dwibahasa Inggris Header: `Name`, `Branch`, `Period`, `Issued on`, `Account Number`, `Currency` ($8.0\text{ pt}$)
   - Header Ringkasan Inggris: `Initial Balance`, `Incoming Transactions`, `Outgoing Transactions`, `Closing Balance` ($8.0\text{ pt}$)
   - Header Tabel Bahasa Inggris: `No`, `Date`, `Remarks`, `Amount (IDR)`, `Balance (IDR)` ($8.0\text{ pt}$)
   - Nomor Halaman Bahasa Inggris: `1 of 18` ($8.0\text{ pt}$)
   - Pemisah Batas Akhir Transaksi: `ini adalah batas akhir transaksi anda` ($8.0\text{ pt}$)
   - Terjemahan Klausul Disclaimer Bahasa Inggris ($8.0\text{ pt}$)

---

## 3. STANDAR WARNA RESMI (HEX & RGB EXACT VALUES)
Berdasarkan ekstraksi telemetry spektrum PDF asli:

| Elemen Dokumen | Kode HEX | Nilai RGB Desimal (0.0 - 1.0) | Keterangan & Penggunaan |
| :--- | :---: | :---: | :--- |
| **Kredit (`+` / Uang Masuk)** | `#06AA6F` | `(0.024, 0.667, 0.435)` | Nominal Kredit tabel mutasi & Header Dana Masuk |
| **Saldo Berjalan & Akhir** | `#134BBA` | `(0.075, 0.294, 0.729)` | Angka Saldo Berjalan tabel & Header Saldo Akhir |
| **Debit (`-` / Uang Keluar)** | `#1A1A1A` | `(0.102, 0.102, 0.102)` | Nominal Debit tabel mutasi & Header Dana Keluar |
| **Saldo Awal Ringkasan** | `#615A5A` | `(0.380, 0.353, 0.353)` | Angka Saldo Awal pada kotak ringkasan Halaman 1 |
| **Legal Footer & Separator** | `#ADA6AE` | `(0.678, 0.651, 0.682)` | Teks legalitas OJK/BI/LPS dan garis pembatas |
| **Teks Putih Banner Header** | `#FFFFFF` | `(1.000, 1.000, 1.000)` | Teks `e-Statement` dan Alamat Bank Mandiri 1 |
| **Teks Hitam Utama** | `#000000` | `(0.000, 0.000, 0.000)` | Label tabel, nomor baris, tanggal, jam, keterangan |

---

## 4. STANDARISASI HEADER DOKUMEN

### A. Banner Biru Atas (Seluruh Halaman)
* **Title `e-Statement`**: $X = 16.00\text{ pt}$, $Y = 34.34\text{ pt}$, Size $16.0\text{ pt}$, Bold, Putih (`#FFFFFF`).
* **Alamat Resmi Bank Mandiri**:
  * Teks: `Menara Mandiri 1 Jalan Jenderal Sudirman Kav. 54-55, Jakarta 12190, Indonesia`
  * Posisi: $X = 300.56\text{ pt}$ s.d. $579.00\text{ pt}$, $Y = 57.42\text{ pt}$, Size $8.0\text{ pt}$, Regular, Putih (`#FFFFFF`).

### B. Metadata Nasabah & Periode (Seluruh Halaman)
* **Baris 1 ($Y = 99.92\text{ pt}$)**:
  * Label `Nama/Name`: $X = 16.00\text{ pt}$ (Nama: Bold, Name: Italic). Titik dua `:` di $X = 111.00\text{ pt}$.
  * **Isi Nama Nasabah**: Dimulai dari $X = 123.00\text{ pt}$, Size $8.0\text{ pt}$, Regular, Format **ALL CAPS**.
    * *Kasus 1 Baris*: Panjang $\le 25$ karakter (contoh: `ROY DARWIN REZERIUS`, `MUHAMMAD NASIH`).
    * *Kasus 2 Baris*: Nama panjang $> 25$ karakter dibagi menjadi:
      * Baris 1: $Y = 96.00\text{ pt}$ ($X = 123.00\text{ pt}$)
      * Baris 2: $Y = 105.00\text{ pt}$ ($X = 123.00\text{ pt}$), tetap aman di atas Cabang ($Y = 121.92\text{ pt}$).
  * Label `Periode/Period`: $X = 233.00\text{ pt}$. Titik dua `:` di $X = 326.00\text{ pt}$.
  * **Isi Periode**: Dimulai dari $X = 340.00\text{ pt}$, Size $8.0\text{ pt}$, Regular (contoh: `01 Aug 2026 - 31 Aug 2026`).
  * **Penomoran Halaman (Indonesia)**: $X = 534.28\text{ pt}$ s.d. $564.00\text{ pt}$, $Y = 99.92\text{ pt}$, Bold (contoh: `1 dari 18`).
* **Baris Sub-Halaman ($Y = 109.92\text{ pt}$)**:
  * **Penomoran Halaman (Inggris)**: $X = 542.40\text{ pt}$ s.d. $564.00\text{ pt}$, $Y = 109.92\text{ pt}$, Italic (contoh: `1 of 18`).
* **Baris 2 ($Y = 121.92\text{ pt}$)**:
  * Label `Cabang/Branch`: $X = 16.00\text{ pt}$. Titik dua `:` di $X = 111.00\text{ pt}$.
  * **Isi Cabang**: Dimulai dari $X = 123.00\text{ pt}$, Size $8.0\text{ pt}$, Regular (contoh: `KCP Jakarta Taman Aries`, `KCP Serang Ciceri`).
  * Label `Dicetak pada/Issued on`: $X = 233.00\text{ pt}$. Titik dua `:` di $X = 326.00\text{ pt}$.
  * **Isi Dicetak**: Dimulai dari $X = 340.00\text{ pt}$, Size $8.0\text{ pt}$, Regular (contoh: `09 Sep 2026`, `22 Jun 2026`).

---

## 5. STANDARISASI KOTAK RINGKASAN FINANSIAL (KHUSUS HALAMAN 1)

Kotak Ringkasan Finansial berada pada rentang $Y = 150.00\text{ pt}$ s.d. $260.00\text{ pt}$:

### A. Bagian Kiri (Informasi Rekening)
* **Tipe Tabungan**: $X = 16.00\text{ pt}$, $Y = 156.88\text{ pt}$, Size $12.0\text{ pt}$, Bold (contoh: `Tabungan NOW IDR`, `Tabungan Mandiri IDR`).
* **Nomor Rekening**:
  * Label `Nomor Rekening/Account Number`: $X = 16.00\text{ pt}$, $Y = 189.92\text{ pt}$, Size $8.0\text{ pt}$. Titik dua `:` di $X = 148.00\text{ pt}$.
  * Nilai Rekening: $X = 160.00\text{ pt}$, $Y = 188.92\text{ pt}$, Size $8.0\text{ pt}$, Regular (contoh: `1650003584860`).
* **Mata Uang**:
  * Label `Mata Uang/Currency`: $X = 16.00\text{ pt}$, $Y = 210.92\text{ pt}$, Size $8.0\text{ pt}$.
  * Nilai: `: IDR` di $X = 148.00\text{ pt}$, $Y = 210.92\text{ pt}$, Size $8.0\text{ pt}$, Regular.

### B. Bagian Kanan (Ringkasan Saldo & Arus Dana)
Titik dua pemisah (`:`) sejajar vertikal di $X = 446.12\text{ pt}$.
**Seluruh angka ringkasan mengunci batas kanan (*Right-Edge*) presisi di $X = 567.00\text{ pt}$**:

1. **Saldo Awal / Initial Balance**:
   * Label: $X = 298.00\text{ pt}$, $Y = 168.92\text{ pt}$.
   * Angka: Right Edge $X = 567.00\text{ pt}$, Warna `#615A5A` (Abu-Abu Gelap), Size $8.0\text{ pt}$ Bold. Format: `6.367.000,81`.
2. **Dana Masuk / Incoming Transactions**:
   * Label: $X = 298.00\text{ pt}$, $Y = 191.92\text{ pt}$.
   * Angka: Right Edge $X = 567.00\text{ pt}$, Warna `#06AA6F` (Hijau Mandiri), Size $8.0\text{ pt}$ Bold. Format: `+ 46.222.000,00` (dengan spasi setelah `+`).
3. **Dana Keluar / Outgoing Transactions**:
   * Label: $X = 298.00\text{ pt}$, $Y = 214.92\text{ pt}$.
   * Angka: Right Edge $X = 567.00\text{ pt}$, Warna `#1A1A1A` (Hitam Pekat), Size $8.0\text{ pt}$ Bold. Format: `- 49.266.970,00` (dengan spasi setelah `-`).
4. **Saldo Akhir / Closing Balance**:
   * Label: $X = 298.00\text{ pt}$, $Y = 238.92\text{ pt}$.
   * Angka: Right Edge $X = 567.00\text{ pt}$, Warna `#134BBA` (Biru Mandiri), Size $8.0\text{ pt}$ Bold. Format: `3.322.030,81`.

**Hukum Rekonsiliasi Neraca:**
$$\text{Saldo Awal} + \text{Dana Masuk} - \text{Dana Keluar} = \text{Saldo Akhir}$$

---

## 6. STANDARISASI GRID TABEL TRANSAKSI

### A. Posisi Vertikal Header Tabel
* **Halaman 1**:
  * Baris Indonesia (Bold): $Y = 295.92\text{ pt}$
  * Baris Inggris (Italic): $Y = 305.92\text{ pt}$
  * Awal Transaksi Baris 1: $Y \approx 339.92\text{ pt}$
* **Halaman 2 s.d. Halaman Terakhir**:
  * Baris Indonesia (Bold): $Y = 179.92\text{ pt}$
  * Baris Inggris (Italic): $Y = 189.92\text{ pt}$
  * Awal Transaksi Baris Pertama Halaman: $Y \approx 217.92\text{ pt}$ s.d. $227.92\text{ pt}$

### B. Koordinat Kolom Tabel Baku (Grid Columns)
1. **Kolom No**:
   * Posisi: Rata Kiri di $X = 20.00\text{ pt}$.
   * Font: $8.0\text{ pt}$ Regular, Warna `#000000`.
   * Terpusat vertikal pada baseline transaksi ($Y_{\text{base}}$).
2. **Kolom Tanggal & Jam**:
   * Posisi: Rata Kiri di $X = 52.00\text{ pt}$.
   * Format Tanggal: `DD Mon YYYY` di $Y = Y_{\text{base}} - 4.00\text{ pt}$ (Regular $8.0\text{ pt}$).
   * Format Jam: `HH:MM:SS WIB` di $Y = Y_{\text{base}} + 5.00\text{ pt}$ (Regular $8.0\text{ pt}$).
3. **Kolom Keterangan (Remarks)**:
   * Posisi: Rata Kiri di $X = 124.00\text{ pt}$.
   * Lebar Area Teks: Maksimum $231.00\text{ pt}$ (Batas kanan $X \approx 355.00\text{ pt}$).
   * Font: $8.0\text{ pt}$ Regular, Warna `#1A1A1A` / `#000000`.
   * Leading / Line Spacing: $\Delta Y = 10.00\text{ pt}$ per baris keterangan.
   * **Struktur Susunan Baris Keterangan terhadap Baseline ($Y_{\text{base}}$)**:
     * **1 Baris** (contoh: `Biaya transfer BI Fast`):
       * Keterangan: $Y = Y_{\text{base}}$
     * **2 Baris** (contoh: `Top-up e-money \n 6032982817401134`):
       * Baris 1: $Y = Y_{\text{base}} - 5.00\text{ pt}$
       * Baris 2: $Y = Y_{\text{base}} + 5.00\text{ pt}$
     * **3 Baris** (contoh: `Transfer BI Fast \n Ke BCA \n DEBORA DIAN FITRESIA 2453460819`):
       * Baris 1: $Y = Y_{\text{base}} - 10.00\text{ pt}$
       * Baris 2: $Y = Y_{\text{base}}$
       * Baris 3: $Y = Y_{\text{base}} + 10.00\text{ pt}$
4. **Kolom Nominal (IDR)**:
   * **Batas Kanan Mutlak (*Right Edge*)**: **$X = 432.00\text{ pt}$**.
   * Font: $8.0\text{ pt}$ Bold, terpusat vertikal di $Y = Y_{\text{base}}$.
   * **Kredit (Dana Masuk)**:
     * Awalan: `+` tanpa spasi (contoh: `+200.000,00`, `+10.000.000,00`).
     * Warna: `#06AA6F` (Hijau Mandiri).
   * **Debit (Dana Keluar)**:
     * Awalan: `-` tanpa spasi (contoh: `-2.500,00`, `-150.000,00`).
     * Warna: `#1A1A1A` (Hitam).
5. **Kolom Saldo (IDR)**:
   * **Batas Kanan Mutlak (*Right Edge*)**: **$X = 571.00\text{ pt}$**.
   * Font: $8.0\text{ pt}$ Bold, terpusat vertikal di $Y = Y_{\text{base}}$.
   * Warna: `#134BBA` (Biru Mandiri).
   * Format: `6.364.500,81` (selalu memiliki 2 angka di belakang koma desimal).

---

## 7. STANDARISASI HALAMAN PENUTUP & DISCLAIMER RESMI

Halaman Terakhir memiliki 3 komponen penutup resmi perbankan:

### A. Garis Penutup Transaksi
* Teks: `ini adalah batas akhir transaksi anda`
* Posisi: Center alignment, $X \approx 234.30\text{ pt}$ s.d. $360.70\text{ pt}$, terletak sekitar $35.00\text{ pt}$ di bawah baris transaksi mutasi terakhir.
* Font: $8.0\text{ pt}$, Italic, Warna `#000000`.

### B. Kotak & Klausul Disclaimer
* **Judul**: `Disclaimer` di $X = 32.00\text{ pt}$, $Y \approx 501.90\text{ pt}$ (atau sesuai akhir tabel), Size $12.0\text{ pt}$ Bold.
* **Format Klausul**: Nomor di $X = 32.00\text{ pt}$, Teks di $X = 47.00\text{ pt}$ s.d. $563.00\text{ pt}$.
* **Klausul 1**:
  * Indo (Regular): `1. e-Statement ini merupakan dokumen elektronik bersifat utuh yang dihasilkan oleh sistem Bank Mandiri dan sah digunakan tanpa tanda tangan dari pejabat Bank Mandri.` *(ejaan otentik: Bank Mandri.)*
  * Inggris (Italic): `/ This e-Statement is an electronic document issued by Bank Mandiri system and is valid for use without an official signature from Bank Mandiri.`
* **Klausul 2**:
  * Indo (Regular): `2. Segala bentuk penggunaan e-Statement ini menjadi tanggung jawab Nasabah sepenuhnya.`
  * Inggris (Italic): `/ All forms of usage of this e-Statement are the Customer's role responsibility.`
* **Klausul 3**:
  * Indo (Regular): `3. Nasabah dapat mengajukan keberatan atas ketidaksesuaian informasi di e-Statement dalam batas waktu 14 hari kalender.`
  * Inggris (Italic): `/ Customers can submit objections regarding information discrepancies in the e-Statement within 14 calendar days.`
* **Klausul 4**:
  * Indo (Regular): `4. Nasabah tunduk dan terikat pada Syarat dan Ketentuan Livin' yang dapat diakses melalui laman resmi Bank Mandiri.`
  * Inggris (Italic): `/ Customers are subject to and bound by the Livin' Term and Conditions which can be accessed via the offical Bank Mandiri website.` *(ejaan otentik: offical)*

### C. Footer Legalitas & Regulasi
Terletak di bagian paling bawah halaman terakhir:
* **Baris 1 ($Y = 809.40\text{ pt}$)**:
  * $X = 26.00\text{ pt}$: `PT Bank Mandiri (Persero) Tbk. berizin dan diawasi oleh Otoritas Jasa Keuangan (OJK) dan Bank Indonesia (BI),` (Warna `#ADA6AE`, Size $8.0\text{ pt}$).
* **Call Center ($Y = 814.40\text{ pt}$)**:
  * $X = 512.50\text{ pt}$ s.d. $579.00\text{ pt}$: `Mandiri Call 14000` (Warna `#ADA6AE`, Size $8.0\text{ pt}$).
* **Baris 2 ($Y = 819.40\text{ pt}$)**:
  * $X = 26.00\text{ pt}$: `serta merupakan peserta penjamin Lembaga Penjamin Simpanan (LPS)` (Warna `#ADA6AE`, Size $8.0\text{ pt}$).

---

## 8. PERBANDINGAN METODE: XARA COPILOT V2 VS PDFCRAFT ENGINE

| Parameter / Fitur | Implementasi di Xara Copilot V2 | Implementasi di PdfCraft Copilot (Standard Baru) |
| :--- | :--- | :--- |
| **Batas Kanan Nominal** | Formula milipoin: $X_{\text{left}} = 431.267\text{ mp} - W$ | Parameter `dx`: $dx = 432.00 - \text{current\_x1}$ atau `align: "right"` |
| **Batas Kanan Saldo** | Formula milipoin: $X_{\text{left}} = 568.306\text{ mp} - W$ | Parameter `dx`: $dx = 571.00 - \text{current\_x1}$ atau `align: "right"` |
| **Pewarnaan Transaksi** | Mencari ID record `Tag 51` dokumen asli (raw binary) | Parameter bawaan: `color: "#06AA6F"`, `"#134BBA"`, `"#1A1A1A"` |
| **Penanganan Split Nodes** | Membersihkan node sekunder via payload `b'\x00\x00'` | Terapkan **Smart Auto-Merge**: node primer diberi teks lengkap, node sekunder diisi `text: ""` |
| **Pergeseran Indeks** | *Zero-Shift Invariant* / Rekalibrasi $\text{Index} + 118$ | **Descending Paragraph Order** (eksekusi paragraf dari nomor terbesar ke terkecil) |
| **Penyusunan Nama 2 Baris** | Menambah 17 record biner + Universal Pointer Recalibration | `text_edit` dengan parameter `width: 90 pt` dan `line_spacing: 0.8` (Zero record drift) |
| **Format File Output** | Biner proprietary Xara (`.xar`) -> Butuh ekspor manual | PDF native langsung (`.pdf`), siap pakai, atomic save |
