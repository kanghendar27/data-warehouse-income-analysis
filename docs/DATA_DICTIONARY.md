# Data Dictionary

## Fact_Pendapatan

| Nama Kolom | Nama Atribut | Tipe Data | Deskripsi | Contoh Nilai |
|------------|-------------|-----------|-----------|--------------|
| id_pendapatan | ID Pendapatan | INT | Primary key, identifikasi unik setiap record pendapatan | 1 |
| id_kk | ID Kepala Keluarga | INT | Foreign key ke Dim_Warga, merujuk pada kepala keluarga | 101 |
| id_pekerjaan | ID Pekerjaan | INT | Foreign key ke Dim_Pekerjaan | 1 |
| id_pendidikan | ID Pendidikan | INT | Foreign key ke Dim_Pendidikan | 3 |
| id_waktu | ID Waktu | INT | Foreign key ke Dim_Waktu | 202601 |
| id_wilayah | ID Wilayah | INT | Foreign key ke Dim_Wilayah | 1 |
| pendapatan | Pendapatan Bulanan | FLOAT | Pendapatan bersih kepala keluarga per bulan dalam Rupiah | 3500000.0 |
| jumlah_tanggungan | Jumlah Tanggungan | INT | Jumlah anggota keluarga yang menjadi tanggungan | 3 |

## Dim_Warga

| Nama Kolom | Nama Atribut | Tipe Data | Deskripsi | Contoh Nilai |
|------------|-------------|-----------|-----------|--------------|
| id_kk | ID Kepala Keluarga | INT | Primary key, identifikasi unik setiap kepala keluarga | 101 |
| nama_kk | Nama Kepala Keluarga | VARCHAR | Nama lengkap kepala keluarga | "Asep Suherman" |
| umur | Umur | INT | Usia kepala keluarga dalam tahun | 42 |
| jenis_kelamin | Jenis Kelamin | VARCHAR | Jenis kelamin kepala keluarga | "Laki-laki" |
| status_rumah | Status Rumah | VARCHAR | Status kepemilikan rumah yang ditempati | "Milik Sendiri" |
| kendaraan | Kendaraan | VARCHAR | Jenis kendaraan utama yang dimiliki | "Motor" |
| bantuan_sosial | Bantuan Sosial | VARCHAR | Jenis bantuan sosial yang diterima (jika ada) | "PKH" |

## Dim_Pekerjaan

| Nama Kolom | Nama Atribut | Tipe Data | Deskripsi | Contoh Nilai |
|------------|-------------|-----------|-----------|--------------|
| id_pekerjaan | ID Pekerjaan | INT | Primary key, identifikasi unik setiap pekerjaan | 1 |
| pekerjaan | Nama Pekerjaan | VARCHAR | Sektor atau jenis pekerjaan utama kepala keluarga | "Buruh Harian" |
| lama_bekerja | Lama Bekerja | INT | Lama bekerja dalam tahun di pekerjaan saat ini | 5 |

## Dim_Pendidikan

| Nama Kolom | Nama Atribut | Tipe Data | Deskripsi | Contoh Nilai |
|------------|-------------|-----------|-----------|--------------|
| id_pendidikan | ID Pendidikan | INT | Primary key, identifikasi unik setiap tingkat pendidikan | 1 |
| pendidikan | Pendidikan Terakhir | VARCHAR | Tingkat pendidikan terakhir yang ditamatkan | "SMA/Sederajat" |

## Dim_Waktu

| Nama Kolom | Nama Atribut | Tipe Data | Deskripsi | Contoh Nilai |
|------------|-------------|-----------|-----------|--------------|
| id_waktu | ID Waktu | INT | Primary key, format YYYYMM | 202601 |
| bulan | Bulan | INT | Bulan dalam angka (1-12) | 1 |
| tahun | Tahun | INT | Tahun pencatatan | 2026 |

## Dim_Wilayah

| Nama Kolom | Nama Atribut | Tipe Data | Deskripsi | Contoh Nilai |
|------------|-------------|-----------|-----------|--------------|
| id_wilayah | ID Wilayah | INT | Primary key, identifikasi unik setiap wilayah | 1 |
| rt | RT | VARCHAR | Nomor Rukun Tetangga | "013" |
| rw | RW | VARCHAR | Nomor Rukun Warga | "004" |
| dusun | Dusun | VARCHAR | Nama dusun | "Ciranggon" |
| desa | Desa | VARCHAR | Nama desa | "Ciranggon" |
| kecamatan | Kecamatan | VARCHAR | Nama kecamatan | "Majalaya" |
| kabupaten | Kabupaten | VARCHAR | Nama kabupaten | "Karawang" |
