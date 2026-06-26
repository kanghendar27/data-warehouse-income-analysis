# Desain Star Schema

## 1. Konsep Star Schema

Star Schema adalah pendekatan pemodelan data dimensional yang menempatkan satu **tabel fakta (fact table)** di pusat yang dikelilingi oleh **tabel dimensi (dimension table)** — membentuk pola seperti bintang. Tabel fakta menyimpan data kuantitatif (measures) dan foreign key ke setiap dimensi, sedangkan tabel dimensi menyimpan data deskriptif (atribut) yang memberikan konteks pada fakta.

Pendekatan ini dipilih karena:
- Sederhana dan mudah dipahami
- Query agregasi cepat (minim JOIN)
- Cocok untuk dashboard Business Intelligence skala kecil

## 2. Diagram Star Schema (ASCII)

```
                                    ┌──────────────────────┐
                                    │                     │
                                    │    Dim_Pekerjaan     │
                                    │                     │
                                    └─────────┬────────────┘
                                              │
                                              │
                    ┌──────────────────┐       │       ┌──────────────────┐
                    │                  │       │       │                  │
                    │   Dim_Pendidikan │───────┼───────│    Dim_Waktu     │
                    │                  │       │       │                  │
                    └──────────────────┘       │       └──────────────────┘
                                              │
                    ┌──────────────────┐       │       ┌──────────────────┐
                    │                  │       │       │                  │
                    │    Dim_Warga     │───────┼───────│   Dim_Wilayah    │
                    │                  │       │       │                  │
                    └──────────────────┘       │       └──────────────────┘
                                              │
                                              │
                                    ┌─────────┴────────────┐
                                    │                     │
                                    │   Fact_Pendapatan   │
                                    │                     │
                                    └──────────────────────┘
```

**Keterangan:**
Setiap dimensi terhubung ke `Fact_Pendapatan` melalui relasi **one-to-many** (satu record dimensi dapat dirujuk oleh banyak record fakta).

## 3. Penjelasan Setiap Tabel

### Fact_Pendapatan

Tabel fakta utama yang menyimpan data pendapatan bulanan setiap Kepala Keluarga. Setiap baris merepresentasikan satu periode pendapatan untuk satu KK pada bulan tertentu. Tabel ini menjadi pusat analisis dan tempat seluruh KPI dihitung.

### Dim_Warga

Menyimpan data demografis setiap Kepala Keluarga. Bersifat *slowly changing dimension* — data hanya berubah jika ada perubahan data KK (misal perubahan status rumah).

### Dim_Pekerjaan

Menyimpan daftar sektor/jenis pekerjaan beserta lama bekerja. Bersifat statis — hanya berisi referensi pekerjaan yang ada di wilayah.

### Dim_Pendidikan

Menyimpan daftar tingkat pendidikan terakhir. Bersifat statis — hanya berisi jenjang pendidikan dari Tidak Sekolah hingga Perguruan Tinggi.

### Dim_Waktu

Menyimpan representasi waktu pencatatan pendapatan. Memudahkan agregasi berdasarkan bulan dan tahun tanpa perlu fungsi tanggal kompleks.

### Dim_Wilayah

Menyimpan hierarki wilayah administratif dari tingkat RT hingga Kabupaten. Bersifat statis — hanya berisi satu wilayah (RT 013 RW 004 Dusun Ciranggon).

## 4. Primary Key

| Tabel | Primary Key | Tipe Data | Keterangan |
|-------|------------|-----------|------------|
| Fact_Pendapatan | id_pendapatan | INT | Auto increment |
| Dim_Warga | id_kk | INT | Auto increment |
| Dim_Pekerjaan | id_pekerjaan | INT | Auto increment |
| Dim_Pendidikan | id_pendidikan | INT | Auto increment |
| Dim_Waktu | id_waktu | INT | Format YYYYMM |
| Dim_Wilayah | id_wilayah | INT | Auto increment |

## 5. Foreign Key

| Tabel Sumber | Foreign Key | Tabel Tujuan | Primary Key |
|-------------|------------|-------------|-------------|
| Fact_Pendapatan | id_kk | Dim_Warga | id_kk |
| Fact_Pendapatan | id_pekerjaan | Dim_Pekerjaan | id_pekerjaan |
| Fact_Pendapatan | id_pendidikan | Dim_Pendidikan | id_pendidikan |
| Fact_Pendapatan | id_waktu | Dim_Waktu | id_waktu |
| Fact_Pendapatan | id_wilayah | Dim_Wilayah | id_wilayah |

## 6. Hubungan Antar Tabel

```
Dim_Warga      ──1──┐
Dim_Pekerjaan  ──1──┤
Dim_Pendidikan ──1──┤──M── Fact_Pendapatan
Dim_Waktu      ──1──┤
Dim_Wilayah    ──1──┘
```

Semua hubungan adalah **one-to-many** dari dimensi ke fakta:
- Satu KK (`Dim_Warga`) dapat memiliki banyak record pendapatan (berbeda bulan).
- Satu pekerjaan (`Dim_Pekerjaan`) dapat dimiliki oleh banyak KK.
- Satu tingkat pendidikan (`Dim_Pendidikan`) dapat dimiliki oleh banyak KK.
- Satu periode waktu (`Dim_Waktu`) dapat mencatat banyak KK.
- Satu wilayah (`Dim_Wilayah`) dapat menampung banyak KK.

## 7. Grain Fact Table

**Grain (granularitas):** Satu baris per Kepala Keluarga per bulan.

Artinya, setiap record di `Fact_Pendapatan` merepresentasikan pendapatan **satu KK pada satu bulan tertentu**. Tidak ada agregasi di level fakta — semua agregasi dilakukan saat query.

## 8. Measures

| Measure | Tipe Data | Deskripsi | Aggregasi Umum |
|---------|-----------|-----------|----------------|
| pendapatan | FLOAT | Pendapatan bersih KK per bulan (Rupiah) | SUM, AVG, MIN, MAX, MEDIAN |
| jumlah_tanggungan | INT | Jumlah anggota keluarga yang menjadi tanggungan | AVG, SUM |

Kedua measure ini adalah **additive**: dapat dijumlahkan atau dirata-rata di seluruh dimensi.

## 9. Dimension Attributes

### Dim_Warga

| Atribut | Tipe Data | Deskripsi |
|---------|-----------|-----------|
| id_kk | INT | Primary key |
| nama_kk | VARCHAR | Nama lengkap kepala keluarga |
| umur | INT | Usia dalam tahun |
| jenis_kelamin | VARCHAR | Laki-laki / Perempuan |
| status_rumah | VARCHAR | Milik Sendiri / Kontrak / Numpang |
| kendaraan | VARCHAR | Motor / Mobil / Tidak Ada |
| bantuan_sosial | VARCHAR | PKH / BPNT / Tidak Ada |

### Dim_Pekerjaan

| Atribut | Tipe Data | Deskripsi |
|---------|-----------|-----------|
| id_pekerjaan | INT | Primary key |
| pekerjaan | VARCHAR | Nama sektor/jenis pekerjaan |
| lama_bekerja | INT | Lama bekerja dalam tahun |

### Dim_Pendidikan

| Atribut | Tipe Data | Deskripsi |
|---------|-----------|-----------|
| id_pendidikan | INT | Primary key |
| pendidikan | VARCHAR | Tingkat pendidikan terakhir |

### Dim_Waktu

| Atribut | Tipe Data | Deskripsi |
|---------|-----------|-----------|
| id_waktu | INT | Primary key (YYYYMM) |
| bulan | INT | Bulan (1–12) |
| tahun | INT | Tahun (2026) |

### Dim_Wilayah

| Atribut | Tipe Data | Deskripsi |
|---------|-----------|-----------|
| id_wilayah | INT | Primary key |
| rt | VARCHAR | Rukun Tetangga |
| rw | VARCHAR | Rukun Warga |
| dusun | VARCHAR | Nama dusun |
| desa | VARCHAR | Nama desa |
| kecamatan | VARCHAR | Nama kecamatan |
| kabupaten | VARCHAR | Nama kabupaten |

## 10. Contoh Record

### Fact_Pendapatan

| id_pendapatan | id_kk | id_pekerjaan | id_pendidikan | id_waktu | id_wilayah | pendapatan | jumlah_tanggungan |
|---------------|-------|-------------|--------------|----------|-----------|-----------|-------------------|
| 1 | 101 | 1 | 3 | 202601 | 1 | 3500000 | 3 |
| 2 | 102 | 2 | 2 | 202601 | 1 | 2800000 | 2 |
| 3 | 103 | 3 | 4 | 202601 | 1 | 4200000 | 4 |
| 4 | 104 | 1 | 1 | 202601 | 1 | 1800000 | 5 |

### Dim_Warga

| id_kk | nama_kk | umur | jenis_kelamin | status_rumah | kendaraan | bantuan_sosial |
|-------|---------|------|---------------|--------------|-----------|----------------|
| 101 | Asep Suherman | 42 | Laki-laki | Milik Sendiri | Motor | PKH |
| 102 | Dede Sunandar | 35 | Laki-laki | Kontrak | Motor | Tidak Ada |
| 103 | Yati Sumiati | 50 | Perempuan | Milik Sendiri | Tidak Ada | BPNT |
| 104 | Jaja Miharja | 28 | Laki-laki | Numpang | Motor | PKH |

### Dim_Pekerjaan

| id_pekerjaan | pekerjaan | lama_bekerja |
|--------------|-----------|-------------|
| 1 | Buruh Harian | 5 |
| 2 | Petani | 10 |
| 3 | Karyawan Swasta | 3 |
| 4 | Pedagang | 7 |

### Dim_Pendidikan

| id_pendidikan | pendidikan |
|--------------|-----------|
| 1 | Tidak Sekolah |
| 2 | SD/Sederajat |
| 3 | SMP/Sederajat |
| 4 | SMA/Sederajat |

### Dim_Waktu

| id_waktu | bulan | tahun |
|----------|-------|-------|
| 202601 | 1 | 2026 |
| 202602 | 2 | 2026 |
| 202603 | 3 | 2026 |
| 202604 | 4 | 2026 |

### Dim_Wilayah

| id_wilayah | rt | rw | dusun | desa | kecamatan | kabupaten |
|------------|-----|-----|--------|-------|-----------|-----------|
| 1 | 013 | 004 | Ciranggon | Ciranggon | Majalaya | Karawang |
