# Sistem Pakar Diagnosis HP Cepat Panas dan Baterai Boros

## 1. Nama dan NIM
- **Nama:** Muhammad Ariq Nabhan
- **NIM:** F1D02510123

## 2. Topik dan Cara Menjalankan
**Topik:** Diagnosis HP Cepat Panas (Overheating) dan Baterai Boros.

**Versi Python:** Python 3.15.2

**Struktur file:**
```
.
├── kb_hp.json
├── mesin_pakar_hp.py
├── README.md
└── screenshot/
    ├── kasus1.png
    ├── kasus2.png
    └── kasus3_negatif.png
```

**Cara menjalankan:**
```bash
python mesin_pakar_hp.py
```
Jawab setiap pertanyaan dengan `y` (ya) atau `t` (tidak).

## 3. Daftar Sumber dan Tabel Aturan

### Daftar Sumber
| Kode | Judul | Penerbit | URL | Tanggal Akses |
|------|-------|----------|-----|---------------|
| S1 | Prevent overheating on your Galaxy device | Samsung Official Support | https://www.samsung.com/us/support/answer/ANS00076952/ | 13 November 2026 |
| S2 | Fix a battery that drains too quickly | Google Android Help | https://support.google.com/android/answer/7664692 | 13 November 2026 |

### Tabel Aturan IF-THEN
| ID | JIKA | Mode | MAKA | Solusi | Sumber |
|----|------|------|------|--------|--------|
| R1 | bodi hp terasa sangat panas saat disentuh **ATAU** muncul notifikasi peringatan suhu perangkat tinggi | atau | indikasi perangkat mengalami overheating | - | S1 |
| R2 | indikasi perangkat mengalami overheating **DAN** sedang digunakan bermain game berat atau rekam video | dan | diagnosis: Overheating karena beban prosesor | Tutup aplikasi dan istirahatkan HP di tempat sejuk | S1 |
| R3 | persentase baterai berkurang sangat drastis **ATAU** hp harus di-charge lebih dari dua kali dalam sehari | atau | indikasi baterai bocor atau boros daya | - | S2 |
| R4 | indikasi baterai bocor atau boros daya **DAN** tingkat kecerahan layar selalu diatur maksimal | dan | diagnosis: Konsumsi daya layar berlebih | Aktifkan fitur kecerahan adaptif otomatis | S2 |
| R5 | indikasi perangkat mengalami overheating **DAN** indikasi baterai bocor atau boros daya | dan | diagnosis: Beban aplikasi latar belakang | Batasi background apps dan perbarui versi software | S2 |

**Rule chaining:** hasil R1 menjadi syarat R2 dan R5, sedangkan hasil R3 menjadi syarat R4 dan R5.

## 4. Metode yang Dipilih
**Forward Chaining.** Metode ini dipilih karena penalaran bergerak maju dari fakta-fakta awal yang dikumpulkan dari pengguna (gejala yang dijawab "y") menuju kesimpulan akhir, dengan aturan yang terpenuhi dieksekusi satu per satu dan hasilnya disimpan ke memori sebagai fakta baru untuk memicu aturan berikutnya.

## 5. Tiga Kasus Uji

| Kasus | Jawaban "y" dari pengguna | Siklus | Kesimpulan |
|-------|---------------------------|--------|------------|
| 1. Satu diagnosis | bodi hp terasa sangat panas; sedang digunakan bermain game berat atau rekam video | R1, R2, berhenti | diagnosis: Overheating karena beban prosesor |
| 2. Kesimpulan ganda (R5 aktif) | bodi hp terasa sangat panas; sedang digunakan bermain game berat atau rekam video; persentase baterai berkurang sangat drastis | R1, R2, R3, R5, berhenti | diagnosis: Overheating karena beban prosesor **dan** diagnosis: Beban aplikasi latar belakang |
| 3. Negatif | hanya tingkat kecerahan layar selalu diatur maksimal | tidak ada aturan terpicu | Tidak ada diagnosis (R4 tidak terpenuhi karena tidak ada indikasi baterai bocor atau boros daya) |

**Kasus 1**

![Kasus 1](screenshot/kasus1.png)

**Kasus 2**

![Kasus 2](screenshot/kasus2.png)

**Kasus 3 (Negatif)**

![Kasus 3](screenshot/kasus3_negatif.png)

## 6. Batas Keberlakuan
Aturan didasarkan pada panduan resmi Samsung dan Google untuk kondisi penggunaan harian, dan hasilnya adalah saran, bukan keputusan akhir mutlak.

## 7. Penggunaan AI
Alat bantu AI (Claude/Gemini) digunakan untuk membantu menyusun kerangka knowledge base JSON, algoritma Forward Chaining di Python, dan penyusunan format Markdown pada README ini.
