# Mini Pipeline MLOps untuk Estimasi Tarif Transportasi Online

Repositori ini berisi mini proyek MLOps Data Mining untuk simulasi pembelajaran estimasi tarif transportasi online.

## Deskripsi Singkat

Proyek ini membangun alur kerja MLOps sederhana mulai dari pemahaman data hingga persiapan presentasi akhir. Model ini memperkirakan `price` (harga) berdasarkan fitur perjalanan seperti jarak, jenis layanan, rute, dan fitur waktu.

Ini hanya simulasi pembelajaran. Bukan sistem pricing *production* nyata.

## Struktur Folder

```text
api/             API FastAPI lokal
data/raw/        Dataset mentah (tidak diubah)
data/processed/  Dataset bersih setelah preprocessing
diagrams/        Diagram pipeline MLOps
models/          Model yang disimpan dan model registry
notebooks/       Notebook Jupyter langkah demi langkah
reports/         Laporan checklist akhir kualitas CI/CT/CD

src/             Kode preprocessing, training, validasi, dan evaluasi
```

## Dataset

- `data/raw/cab_rides.csv`
- `data/processed/cleaned_cab_rides.csv`

Data awal berjumlah 693.071 baris. Setelah dibersihkan tersisa 637.976 baris.

## Instruksi Download Dataset

Dataset tidak disertakan di repositori GitHub ini karena ukurannya besar.

Sumber dataset:
https://www.kaggle.com/datasets/ravi72munde/uber-lyft-cab-prices

Setelah melakukan clone, unduh dataset secara manual dari Kaggle dan simpan di:

```text
data/raw/cab_rides.csv
```

Jalankan notebook preprocessing untuk menghasilkan data bersih:

```text
notebooks/02_preprocessing_baseline_model.ipynb
```

Hasilnya akan tersimpan di:

```text
data/processed/cleaned_cab_rides.csv
```

## Cara Menjalankan Notebook

Buka notebook secara berurutan dan jalankan (Run All):

1. `notebooks/01_data_understanding.ipynb`
2. `notebooks/02_preprocessing_baseline_model.ipynb`
3. `notebooks/03_model_evaluation_quality_checklist.ipynb`
4. `notebooks/04_cd_scenario_pipeline_design.ipynb`

## Cara Menjalankan API Lokal

Install library:

```bash
pip install fastapi uvicorn joblib pandas scikit-learn
```

Jalankan dari root folder:

```bash
uvicorn api.app:app --reload
```

Contoh *request body* ada di `api/request_example.json`.

## Hasil Model Utama

- Target prediksi: `price`
- Jenis masalah: Regresi
- Model terbaik: Random Forest Regressor
- Versi model: `v1.0-baseline-random-forest`
- MAE: 1.4254
- RMSE: 2.6181
- R2 Score: 0.9214

## Catatan Penting

Proyek ini murni simulasi pembelajaran. Model ini tidak boleh digunakan sebagai sistem pricing sungguhan. API hanya berjalan di localhost.

## Anggota Kelompok

- Abyan Hisyam Al'Ammar
- Lavina Arsya Aryanto
- Muhamad Fikih Rizaldi
- Daffa Akmal Ayom Pamungkas
- Desta Adriyan Saputra
