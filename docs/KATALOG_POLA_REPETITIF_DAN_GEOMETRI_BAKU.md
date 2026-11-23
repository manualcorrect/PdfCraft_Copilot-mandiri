# KATALOG POLA REPETITIF & GEOMETRI BAKU E-STATEMENT
## Pedoman Presisi Posisi Teks & Angka untuk PdfCraft Copilot
**Status:** Permanent Mathematical & Geometric Specification  
**Basis Data:** Telemetri PDF Asli ([Agu 2026_unlocked.pdf](file:///D:/X_Files/rekening/Reference/Roy/ilovepdf_unlocked/Agu%202026_unlocked.pdf) & [e-Statement_XXXXXXXXX9210_01 Des 2024-31 Des 2024_unlocked.pdf](file:///D:/X_Files/rekening/Reference/nasih%202024%20new%20unlocked/ilovepdf_unlocked/e-Statement_XXXXXXXXX9210_01%20Des%202024-31%20Des%202024_unlocked.pdf))

---

## 1. POLA GRID TABEL TRANSAKSI & FORMULA INTERVAL $dY = 46.00\text{ pt}$

Seluruh baris transaksi pada kedua dokumen referensi mengikuti aturan interval vertikal konstan sebesar **$dY = 46.00\text{ pt}$**:

```
[Baris N]   ─── Y_base(N) ─────────────────────────────
                  │
                  ▼  dY = +46.00 pt (Interval Konstan Absolut)
                  │
[Baris N+1] ─── Y_base(N+1) = Y_base(N) + 46.00 pt ────
```

### A. Formula Baseline Vertikal Baris Transaksi ($Y_{\text{base}}$)
1. **Halaman 1 (Terdapat Kotak Ringkasan Finansial)**:
   $$Y_{\text{base}}(\text{Page 1}, \text{row } i) = 343.92 + (i - 1) \times 46.00\text{ pt}\quad (i = 1 \dots 10)$$
   * Baris 1: $Y = 343.92\text{ pt}$
   * Baris 2: $Y = 389.92\text{ pt}$
   * Baris 3: $Y = 435.92\text{ pt}$
   * Baris 4: $Y = 481.92\text{ pt}$
   * Baris 5: $Y = 527.92\text{ pt}$
   * Baris 6: $Y = 573.92\text{ pt}$
   * Baris 7: $Y = 619.92\text{ pt}$
   * Baris 8: $Y = 665.92\text{ pt}$
   * Baris 9: $Y = 711.92\text{ pt}$
   * Baris 10: $Y = 757.92\text{ pt}$
   * **Kapasitas Halaman 1**: Persis **10 baris transaksi**.

2. **Halaman 2 s.d. Halaman Sebelum Terakhir (Halaman Penuh)**:
   $$Y_{\text{base}}(\text{Page } P, \text{row } j) = 227.92 + (j - 1) \times 46.00\text{ pt}\quad (j = 1 \dots 12, P \ge 2)$$
   * Baris 1 (di halaman tsb): $Y = 227.92\text{ pt}$
   * Baris 2: $Y = 273.92\text{ pt}$
   * Baris 3: $Y = 319.92\text{ pt}$
   * Baris 4: $Y = 365.92\text{ pt}$
   * Baris 5: $Y = 411.92\text{ pt}$
   * Baris 6: $Y = 457.92\text{ pt}$
   * Baris 7: $Y = 503.92\text{ pt}$
   * Baris 8: $Y = 549.92\text{ pt}$
   * Baris 9: $Y = 595.92\text{ pt}$
   * Baris 10: $Y = 641.92\text{ pt}$
   * Baris 11: $Y = 687.92\text{ pt}$
   * Baris 12: $Y = 733.92\text{ pt}$
   * **Kapasitas Halaman Penuh**: Persis **12 baris transaksi**.

3. **Halaman Terakhir (Bersama Disclaimer)**:
   * Menggunakan titik awal yang sama: $Y = 227.92 + (k - 1) \times 46.00\text{ pt}$.
   * **Kapasitas Maksimal Halaman Penutup**: **Maksimal 7 baris transaksi** (Baris terakhir $Y \le 503.92\text{ pt}$) agar tidak menabrak Disclaimer dan Legal Footer.

---

## 2. POLA RELASI VERTIKAL DI DALAM SETIAP BARIS TRANSAKSI

Setiap elemen dalam satu transaksi memiliki posisi relatif yang terkunci terhadap **$Y_{\text{base}}$**:

| Elemen Transaksi | Formula Posisi Vertikal ($Y$) | Offset terhadap $Y_{\text{base}}$ | Font & Style |
| :--- | :---: | :---: | :--- |
| **Nomor Urut (`No`)** | $Y = Y_{\text{base}}$ | $0.00\text{ pt}$ | Regular $8.0\text{ pt}$ |
| **Tanggal Mutasi** | $Y = Y_{\text{base}} - 4.00\text{ pt}$ | $-4.00\text{ pt}$ (Lebih ke atas) | Regular $8.0\text{ pt}$ |
| **Jam Mutasi** | $Y = Y_{\text{base}} + 5.00\text{ pt}$ | $+5.00\text{ pt}$ (Lebih ke bawah) | Regular $8.0\text{ pt}$ (`HH:MM:SS WIB`) |
| **Nominal (IDR)** | $Y = Y_{\text{base}}$ | $0.00\text{ pt}$ | Bold $8.0\text{ pt}$ |
| **Saldo (IDR)** | $Y = Y_{\text{base}}$ | $0.00\text{ pt}$ | Bold $8.0\text{ pt}$ |

### Pola Simetri Baris Keterangan terhadap $Y_{\text{base}}$:
Semua baris uraian transaksi dimulai dari $X = 124.00\text{ pt}$ dengan line spacing $\Delta Y = 10.00\text{ pt}$:

* **Kasus 1 Baris** (contoh: `Biaya transfer BI Fast`):
  $$\text{Baris 1} = Y_{\text{base}}$$
* **Kasus 2 Baris** (contoh: `Top-up e-money` / `6032982817401134`):
  $$\text{Baris 1} = Y_{\text{base}} - 5.00\text{ pt},\quad \text{Baris 2} = Y_{\text{base}} + 5.00\text{ pt}$$
* **Kasus 3 Baris** (contoh: `Transfer BI Fast` / `Ke BCA` / `DEBORA DIAN FITRESIA 2453460819`):
  $$\text{Baris 1} = Y_{\text{base}} - 10.00\text{ pt},\quad \text{Baris 2} = Y_{\text{base}},\quad \text{Baris 3} = Y_{\text{base}} + 10.00\text{ pt}$$
* **Kasus 4 Baris** (contoh: `Transfer antar Mandiri` / `DARI KOPERASI KONSUMEN...` / `DTL - Kopkar...` / `Transfer Fee`):
  $$\text{Baris 1} = Y_{\text{base}} - 15.00\text{ pt},\quad \text{Baris 2} = Y_{\text{base}} - 5.00\text{ pt},\quad \text{Baris 3} = Y_{\text{base}} + 5.00\text{ pt},\quad \text{Baris 4} = Y_{\text{base}} + 15.00\text{ pt}$$

---

## 3. POLA PENJAJARAN HORIZONTAL SUMBU X (ALIGNMENT ANCHORS)

Terdapat 5 garis imajiner (*ruler guides*) vertikal yang mengunci seluruh halaman dokumen:

```
X=20.0pt     X=52.0pt        X=124.0pt                 X_right=432.0pt    X_right=571.0pt
  │            │               │                             │                  │
 [No]      [Tanggal]      [Keterangan]                 [Nominal(IDR)]      [Saldo(IDR)]
  │        [  Jam  ]           │                             │                  │
(Left)       (Left)          (Left)                       (Right)            (Right)
```

1. **Jangkar Kiri No**: $X = 20.00\text{ pt}$ (Rata Kiri).
2. **Jangkar Kiri Tanggal & Jam**: $X = 52.00\text{ pt}$ (Rata Kiri, tegak lurus sejajar).
3. **Jangkar Kiri Keterangan**: $X = 124.00\text{ pt}$ (Rata Kiri, lebar maksimal $231\text{ pt}$).
4. **Jangkar Kanan Nominal**: **Batas Kanan Mutlak di $X = 432.00\text{ pt}$** (Rata Kanan).
   - Berapa pun jumlah digitnya (ratusan rupiah, jutaan, hingga ratusan juta), tanda koma `,00` selalu lurus di garis $432.00\text{ pt}$.
5. **Jangkar Kanan Saldo**: **Batas Kanan Mutlak di $X = 571.00\text{ pt}$** (Rata Kanan).
   - Tanda desimal `,00` / `,81` selalu mengunci lurus di garis $571.00\text{ pt}$.

---

## 4. POLA RINGKASAN FINANSIAL HEADER (HALAMAN 1)

* **Jangkar Titik Dua (`:`):** Seluruh titik dua sejajar vertikal di $X = 446.12\text{ pt}$.
* **Jangkar Kanan Angka Ringkasan:** **Batas Kanan Mutlak di $X = 567.00\text{ pt}$**.
* **Interval Vertikal Ringkasan:**
  * Saldo Awal: $Y = 168.92\text{ pt}$
  * Dana Masuk: $Y = 191.92\text{ pt}$ ($\Delta Y = +23.00\text{ pt}$)
  * Dana Keluar: $Y = 214.92\text{ pt}$ ($\Delta Y = +23.00\text{ pt}$)
  * Saldo Akhir: $Y = 238.92\text{ pt}$ ($\Delta Y = +24.00\text{ pt}$)

---

## 5. POLA PENUTUP TRANSAKSI & DISCLAIMER (HALAMAN TERAKHIR)

Posisi vertikal bagian penutup dihitung secara dinamis dari posisi transaksi terakhir ($Y_{\text{last\_row}}$):

1. **Teks `ini adalah batas akhir transaksi anda`**:
   $$Y_{\text{batas\_akhir}} = Y_{\text{last\_row}} + 38.00\text{ pt}$$
   * Terpusat secara horizontal di tengah halaman: $X \approx 234.30 - 360.70\text{ pt}$ ($8.0\text{ pt}$ Italic).
2. **Judul `Disclaimer`**:
   $$Y_{\text{disclaimer\_title}} = Y_{\text{batas\_akhir}} + 52.00\text{ pt} = Y_{\text{last\_row}} + 90.00\text{ pt}$$
   * Posisi: $X = 32.00\text{ pt}$, Size $12.0\text{ pt}$ Bold.
3. **Klausul 1 s.d. 4 Disclaimer**:
   * Klausul 1: $Y = Y_{\text{disclaimer\_title}} + 25.00\text{ pt}$
   * Klausul 2: $Y = Y_{\text{disclaimer\_title}} + 70.00\text{ pt}$
   * Klausul 3: $Y = Y_{\text{disclaimer\_title}} + 99.00\text{ pt}$
   * Klausul 4: $Y = Y_{\text{disclaimer\_title}} + 132.00\text{ pt}$
4. **Footer Regulasi & Mandiri Call 14000 (Terkunci di Bawah Halaman)**:
   * Baris 1: $Y = 809.40\text{ pt}$ ($X = 26.00\text{ pt}$)
   * Call Center: $Y = 814.40\text{ pt}$ ($X = 512.50 - 579.00\text{ pt}$)
   * Baris 2: $Y = 819.40\text{ pt}$ ($X = 26.00\text{ pt}$)

---

## 6. MATRIKS DIAGNOSTIK KESALAHAN POSISI & FORMULA PEMULIHAN PDFCRAFT

Saat dokumen baru dibuka dan diinspeksi, tabel berikut digunakan sebagai filter otomatis untuk mendeteksi deviasi posisi:

| Gejala Kesalahan Posisi | Nilai Terdeteksi (*Faulty*) | Standar Baku (*Reference*) | Formula Pemulihan di PdfCraft |
| :--- | :--- | :--- | :--- |
| **Nominal Tidak Rata Kanan** | $X_1 \ne 432.00\text{ pt}$ | $X_1 = 432.00\text{ pt}$ | Panggil `text_edit` dengan parameter `dx = 432.00 - current_x1` |
| **Saldo Tidak Rata Kanan** | $X_1 \ne 571.00\text{ pt}$ | $X_1 = 571.00\text{ pt}$ | Panggil `text_edit` dengan parameter `dx = 571.00 - current_x1` |
| **Ringkasan Saldo Melenceng** | $X_1 \ne 567.00\text{ pt}$ | $X_1 = 567.00\text{ pt}$ | Panggil `text_edit` dengan parameter `dx = 567.00 - current_x1` |
| **Tanggal / Jam Melorot/Miring** | $X_0 \ne 52.00\text{ pt}$ | $X_0 = 52.00\text{ pt}$ | Panggil `text_edit` dengan parameter `dx = 52.00 - current_x0` |
| **Nomor Urut Melenceng** | $X_0 \ne 20.00\text{ pt}$ | $X_0 = 20.00\text{ pt}$ | Panggil `text_edit` dengan parameter `dx = 20.00 - current_x0` |
| **Keterangan Tidak Sejajar Kolom** | $X_0 \ne 124.00\text{ pt}$ | $X_0 = 124.00\text{ pt}$ | Panggil `text_edit` dengan parameter `dx = 124.00 - current_x0` |
| **Jam & Menit Terbelah Dua Box** | 2 paragraf (`HH` dan `:MM:SS`) | 1 paragraf utuh | Kotak 1: `text: "HH:MM:SS WIB"`, `width: 50`. Kotak 2: `text: ""` |
| **Keterangan Terbelah Dua Box** | Baris 1 & 2 terpisah paragraf | 1 paragraf multi-baris | Kotak 1: teks utuh (`\n`), `width: 220`. Kotak 2: `text: ""` |
| **Warna Kredit Bukan Hijau** | Hitam / Abu | `#06AA6F` | Panggil `text_edit` dengan parameter `color: "#06AA6F"` |
| **Warna Saldo Bukan Biru** | Hitam | `#134BBA` | Panggil `text_edit` dengan parameter `color: "#134BBA"` |
| **Warna Debit Bukan Hitam** | Hijau / Abu | `#1A1A1A` | Panggil `text_edit` dengan parameter `color: "#1A1A1A"` |
| **Warna Saldo Awal Bukan Abu** | Hitam | `#615A5A` | Panggil `text_edit` dengan parameter `color: "#615A5A"` |
| **Baris Menumpuk / Interval Kacau** | $dY \ne 46.00\text{ pt}$ | $dY = 46.00\text{ pt}$ | Sesuaikan $Y_{\text{base}}$ baris target menggunakan parameter `dy` |
