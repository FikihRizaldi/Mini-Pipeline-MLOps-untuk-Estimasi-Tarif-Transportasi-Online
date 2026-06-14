# Checklist Kualitas Akhir

Checklist ini menggabungkan metrik CI, CT, dan CD agar mudah dimasukkan ke laporan akhir atau slide presentasi.

## Tabel 1 - Checklist CI

| Nama Pengecekan | Aturan | Status | Catatan |
|---|---|---|---|
| Kolom wajib tersedia | Kolom wajib harus tersedia | PASS | `price`, `distance`, `cab_type`, `source`, `destination`, `name`, dan `time_stamp` tersedia. |
| Target price tidak null | `price` tidak boleh kosong pada data training | PASS | Baris tanpa target sudah dibuang saat *cleaning*. |
| distance > 0 | `distance` harus lebih besar dari 0 | PASS | Tidak ada jarak yang tak valid pada data bersih. |
| price > 0 | `price` harus lebih besar dari 0 | PASS | Tidak ada harga yang tak valid pada data bersih. |
| source tidak null | `source` tidak boleh kosong | PASS | Kolom lengkap. |
| destination tidak null | `destination` tidak boleh kosong | PASS | Kolom lengkap. |
| cab_type tidak null | `cab_type` tidak boleh kosong | PASS | Kolom lengkap. |
| name tidak null | `name` tidak boleh kosong | PASS | Kolom lengkap. |
| time_stamp bisa dikonversi | `time_stamp` harus bisa dikonversi ke datetime | PASS | Timestamp valid untuk *feature engineering* waktu. |
| Tidak ada duplikat persis | Tidak boleh ada *duplicate row* yang sama persis | PASS | Duplikat sudah dicek dan aman. |

## Tabel 2 - Checklist CT

| Nama Pengecekan | Metrik / Aturan | Nilai Saat Ini | Batas (Threshold) | Status | Catatan |
|---|---|---:|---:|---|---|
| Cek ambang batas MAE | MAE harus rendah | 1.4254 | <= 2.00 | PASS | Error rata-rata masih dalam batas *baseline*. |
| Cek ambang batas RMSE | RMSE harus rendah | 2.6181 | <= 3.50 | PASS | Error ekstrem masih cukup terkendali. |
| Cek skor R2 | R2 harus cukup tinggi | 0.9214 | >= 0.85 | PASS | Model bisa menjelaskan variasi target dengan sangat baik. |
| Error berdasarkan jarak | Group MAE tidak terlalu tinggi | Long trip MAE 1.8285 | Monitor | PASS | Jarak jauh memiliki error tertinggi di kategorinya, tapi masih wajar. |
| Error by cab_type | Group MAE tidak terlalu tinggi | Lyft MAE 1.6723 | Monitor | PASS | Perbedaan antar perusahaan taksi perlu terus dipantau. |
| Error by service name | Service MAE tidak terlalu tinggi | Lux Black XL MAE 2.9136 | Monitor | WARNING | Lux Black XL adalah layanan dengan prediksi meleset paling tinggi. |
| Review distribusi error prediksi | Distribusi error perlu dicek manual | Direview | Cek tiap iterasi | PASS | Plot error sudah dibuat di notebook evaluasi. |
| Review kekuatan model jarak dekat/jauh | Perjalanan pendek & jauh harus wajar | Direview | Cek tiap iterasi | PASS | Review berbasis kelompok jarak sudah masuk checklist. |

## Tabel 3 - Checklist CD

| Komponen CD | Pilihan Desain | Status | Catatan |
|---|---|---|---|
| Format model | `.joblib` | READY | Model tersimpan dengan baik di `models/baseline_price_model.joblib`. |
| Model registry | `models/model_registry.json` | READY | Memuat versi model, metrik evaluasi, status persetujuan, dan catatan peringatan. |
| Framework API | FastAPI | READY | *Skeleton* kode lokal tersedia di `api/app.py`. |
| Endpoint prediksi | `/predict` | READY | Menerima fitur rute/jarak dan mengembalikan estimasi tarif. |
| Deployment strategy | Shadow Deployment | DESIGNED | Model baru berjalan dan diuji di *background* terlebih dahulu secara diam-diam. |
| Rollback strategy | Versi *approved* sebelumnya | DESIGNED | Bila hasil monitoring buruk, sistem kembali menggunakan model yang stabil. |
| Monitoring metrics | MAE, RMSE, R2, group MAE | DESIGNED | Alat ukur utama untuk menilai model pasca rilis simulasi. |
| Rencana logging | Input, output, waktu, versi model | PLANNED | Belum berbentuk layanan, baru sebatas rancangan arsitektur. |
| Catatan keamanan | Hanya simulasi MLOps | DOCUMENTED | Bukan untuk mengatur harga bagi pengguna asli. |
