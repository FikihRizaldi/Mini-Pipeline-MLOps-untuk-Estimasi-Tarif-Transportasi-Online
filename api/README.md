# Local Fare Estimation API

Folder ini berisi skeleton API lokal FastAPI. Ini simulasi pembelajaran, bukan pricing system produksi.

## Install Library

```bash
pip install fastapi uvicorn joblib pandas scikit-learn
```

## Jalankan Lokal

Jalankan dari root folder:

```bash
uvicorn api.app:app --reload
```

Lalu buka:

```text
http://127.0.0.1:8000/
```

## Contoh Request

Kirim request `POST` ke:

```text
http://127.0.0.1:8000/predict
```

Contoh body:

```json
{
  "distance": 2.5,
  "cab_type": "Uber",
  "source": "Back Bay",
  "destination": "North End",
  "name": "UberX",
  "time_stamp": 1544952607890
}
```

Contoh yang sama ada di `api/request_example.json`.

## Contoh Response

```json
{
  "estimated_price": 10.75,
  "model_version": "v1.0-baseline-random-forest",
  "note": "This is a learning simulation for fare estimation, not a real production pricing system."
}
```

Harga estimasi bisa beda tergantung versi model.

## Keterbatasan

- API ini hanya demo lokal.
- Tidak di-deploy ke cloud.
- Tidak pakai `surge_multiplier`.
- Tidak butuh `price` karena itu target.
- Data cuaca belum digabung.
- Tidak boleh dipakai untuk menentukan harga nyata.
