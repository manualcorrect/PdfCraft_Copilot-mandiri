# PENYESUAIAN TEKNIKAL & PANDUAN TROUBLESHOOTING
## Solusi Kasus Khusus (*Edge Cases*) pada PdfCraft Copilot

Dokumen ini mencatat seluruh temuan teknis mendalam (*deep forensic insights*), kendala yang dihadapi selama pengembangan, serta arsitektur solusi baku yang diimplementasikan pada **PdfCraft Copilot**.

---

## 1. Masalah: Pergeseran Indeks Paragraf (*Paragraph Index Drift*)

### Gejala
Ketika melakukan pengeditan atau penggantian beberapa baris teks dalam satu halaman secara berurutan dari atas ke bawah (indeks $0 \dots M$), penambahan atau pengurangan baris menyebabkan struktur pohon objek bergeser. Paragraf berikutnya yang ditargetkan meleset ke elemen lain.

### Solusi Baku: **Descending Traversal Order**
Semua manipulasi teks dilakukan dengan mengurutkan target dari posisi/indeks terbesar ke terkecil:
```python
# Urutkan dari elemen paling bawah ke paling atas
targets.sort(key=lambda item: item['index'], reverse=True)
for item in targets:
    editor.edit_paragraph(item['index'], new_text)
```
Dengan memodifikasi node bawah terlebih dahulu, indeks node atas tetap stabil (*Zero-Shift Invariant*).

---

## 2. Masalah: Kerusakan Encoding Font Embedded (`Type0 / Identity-H`)

### Gejala
PDF perbankan resmi menggunakan font `TTInterphases` yang disematkan (*embedded subset*). Jika teks diedit menggunakan library PDF standar dengan metode penulisan string ANSI biasa, karakter akan muncul sebagai kotak kosong (*missing glyphs*), karakter tanda tanya, atau font fallback yang tidak seragam (misal: Helvetica).

### Solusi Baku: **Low-Level FlateDecode Stream Replacement**
Untuk elemen-elemen presisi seperti nomor halaman, nama cabang, dan nilai ringkasan, engine melakukan bypass terhadap parser tingkat tinggi:
1. Membaca stream konten halaman biner (`/Contents`).
2. Melakukan dekompresi menggunakan `zlib.decompress`.
3. Mengganti string biner atau kode heksadesimal UTF-16BE / CID:
   ```python
   def to_utf16_be_hex(text: str) -> str:
       return ''.join(f'{ord(c):04X}' for c in text)
   ```
4. Melakukan rekompresi stream (`zlib.compress(modified_stream)`) dan memperbarui panjang objek (`/Length`).

Metode ini menjamin 100% font subset asli tetap utuh tanpa merusak tabel ToUnicode internal PDF.

---

## 3. Masalah: Presisi Rata Kanan Angka Keuangan (*Right-Edge Invariance*)

### Gejala
Jumlah digit nominal transaksi berbeda-beda:
* Ratusan ribu: `-250.000,00` (11 karakter)
* Puluhan juta: `+15.000.000,00` (14 karakter)
* Ratusan juta: `+125.000.000,00` (15 karakter)

Jika menggunakan titik awal kiri ($X_{\text{left}}$) yang statis, tanda desimal koma `,00` akan berantakan dan tidak sejajar vertikal.

### Solusi Baku: **Formula Delta Penjajaran Kanan**
Batas kanan mutlak ditetapkan pada:
* Kolom Nominal: $X_{\text{right}} = 432.00\text{ pt}$
* Kolom Saldo: $X_{\text{right}} = 571.00\text{ pt}$
* Angka Kotak Ringkasan: $X_{\text{right}} = 567.00\text{ pt}$

Sebelum merender angka, sistem menghitung lebar string aktual $W$ berdasarkan metrik glif `TTInterphases-Bold` ($8.0\text{ pt}$), lalu menempatkan titik awal di:
$$X_{\text{left}} = X_{\text{right}} - W$$
Atau menerapkan offset pergeseran:
$$dx = X_{\text{right}} - \text{current\_x1}$$
Hasilnya, koma desimal `,00` selalu sejajar presisi 100% pada garis pandu.

---

## 4. Masalah: Pemisahan Nama Nasabah Panjang (> 25 Karakter)

### Gejala
Nama nasabah seperti `ROY DARWIN REZERIUS` atau nama perusahaan dapat melebihi batas kolom nama dan berisiko menabrak label `Periode` di $X = 233.00\text{ pt}$ atau menabrak baris `Cabang` di $Y = 121.92\text{ pt}$.

### Solusi Baku: **Dua Baris Terkendali Spasial**
* Jika panjang nama $\le 25$ karakter:
  * Ditulis 1 baris pada koordinat standar $X = 123.00\text{ pt}, Y = 99.92\text{ pt}$.
* Jika panjang nama $> 25$ karakter:
  * Dipecah secara semantik pada batas spasi kata.
  * **Baris 1**: $X = 123.00\text{ pt}, Y = 96.00\text{ pt}$
  * **Baris 2**: $X = 123.00\text{ pt}, Y = 105.00\text{ pt}$
  * Jarak aman vertikal tetap terjaga di atas label Cabang ($Y = 121.92\text{ pt}$) tanpa tumpang tindih.

---

## 5. Masalah: Tabrakan Jam & Pola Tanggal (*Chronological Collision*)

### Gejala
Ketika mengimpor puluhan transaksi dalam 1 hari yang sama, penentuan jam secara acak dapat menyebabkan:
1. Jam transaksi melompat mundur (inkonsistensi kronologis).
2. Transaksi payroll korporat jatuh pada tengah malam atau hari libur.

### Solusi Baku: **Smart Chronological Generator**
Modul `src/smart_date_time_generator.py` menerapkan aturan:
* Waktu awal hari dimulai antara jam 07:30 s.d. 08:30 WIB.
* Setiap transaksi berikutnya dalam hari yang sama wajib memiliki interval positif $\Delta t \in [3, 45]$ menit.
* Transaksi Corporate Payroll secara otomatis dialokasikan pada hari kerja di jendela jam operasional perbankan (08:00 - 15:00 WIB).

---

## 7. Masalah: Dekompresi Stream Terpotong (`zlib.error: Error -5 truncated stream`)

### Gejala
Ketika membaca objek stream terkompresi menggunakan ekspresi reguler greedy seperti `stream[\r\n]+(.*?)[\r\n]+endstream`, byte terakhir dari data biner kompresi yang bernilai `\r` (0x0D) atau `\n` (0x0A) secara keliru tertelan sebagai pemisah (*delimiter*), mengakibatkan `zlib.error: Error -5 while decompressing data: incomplete or truncated stream`.

### Solusi Baku: **Exact `/Length <N>` Byte Slicing**
Engine beralih menggunakan pemotongan biner eksak sesuai header kamus PDF:
```python
m_len = re.search(rb'/Length\s+(\d+)', raw_obj)
length = int(m_len.group(1))
m_stream = re.search(rb'stream(\r\n|\n)', raw_obj)
stream_bytes = raw_obj[m_stream.end() : m_stream.end() + length]
decompressed = zlib.decompress(stream_bytes)
```
Metode ini 100% kebal terhadap variasi byte acak pada ujung stream biner.

---

## 8. Logika Pasangan Transaksi Biller & Biaya Penutup Bulan

### Gejala & Temuan Forensik
1. **Pasangan Transaksi Biller**: Setiap transaksi topup e-wallet (`Pembayaran Danatopup`) pada sistem Livin' Mandiri selalu didahului oleh transaksi `Biaya transaksi bank` (-Rp 1.000) dengan tanggal dan detik yang persis identik (*synchronized timestamps*). Jika ada mutasi debit mandiri (misal -Rp 450.000) tanpa biaya admin, mutasi tersebut secara logis dan otentik adalah transaksi `Penarikan tunai di ATM` (2 baris: jenis transaksi + nama lokasi ATM).
2. **Penutup Akhir Bulan (`Biaya administrasi rekening`)**: Diletakkan pada tanggal terakhir bulan pukul `23:59:00 WIB` dengan nominal -Rp 5.000 atau -Rp 12.500. Keterangan ini berformat 1 baris yang wajib duduk persis pada baseline baris `top = 734.00 pt` (menerapkan offset translasi `dy = -5.0 pt` dari bounding box bawaan).

---

## 9. Rekonsiliasi Saldo Integer Excel vs Desimal PDF

Untuk memastikan neraca akuntansi tetap klop 100% pada kedua media:
* **Tabel Mutasi Excel**: Kolom Saldo disimpan sebagai integer murni (`running_saldo_int = saldo_awal_int + sum(nominals)`).
* **e-Statement PDF**: Ditambahkan desimal sen baku `,81` (`format_idr(running_saldo_int + 0.81)`).
Hal ini mencegah deviasi $\pm 1$ rupiah akibat pembulatan *float* (`round`) pada digit sen.

---

## 10. Checklist Pemecahan Masalah di Perangkat Baru

| Masalah | Kemungkinan Penyebab | Tindakan Solusi |
| :--- | :--- | :--- |
| `ModuleNotFoundError: No module named 'pdfplumber'` | Dependensi belum terinstal | Jalankan `pip install -r requirements.txt`. |
| Font tampak berbeda di PDF viewer Linux | Pembaca PDF menggunakan subsitusi lokal | Buka dokumen menggunakan browser (Chrome/Edge) atau Adobe Acrobat yang mematuhi embedded font Identity-H. |
| Angka saldo tidak balance | Data di Excel memiliki selisih input manual | Buka file Excel, periksa baris transaksi yang selisih, jalankan parser untuk auto-reconcile. |
