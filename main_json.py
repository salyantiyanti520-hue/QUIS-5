import json
from pathlib import Path
from typing import Any

# File JSON input dan output berada di folder yang sama dengan main.py
INPUT_JSON = Path("data.json")
OUTPUT_JSON = Path("hasil_pengolahan.json")


def buat_data_contoh() -> list[dict[str, Any]]:
    """Data contoh digunakan jika data.json belum tersedia."""
    return [
        {"id": 1, "nama": "Salyanti", "umur": 20, "nilai": 85, "aktif": True},
        {"id": 2, "nama": "Budi", "umur": 17, "nilai": 70, "aktif": False},
        {"id": 3, "nama": "Citra", "umur": 21, "nilai": 92, "aktif": True},
        {"id": 4, "nama": "Dina", "umur": 19, "nilai": 60, "aktif": True},
        {"id": 5, "nama": "Eko", "umur": 22, "nilai": 78, "aktif": False},
    ]


def baca_json(path: Path) -> list[dict[str, Any]]:
    """Membaca data dari file JSON."""
    if not path.exists():
        print(f"File {path} belum ditemukan. Menggunakan data contoh.")
        return buat_data_contoh()

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(f"Format JSON pada {path} tidak valid: {error}") from error

    if not isinstance(data, list):
        raise ValueError("Isi data.json harus berupa JSON array/list.")

    if not all(isinstance(item, dict) for item in data):
        raise ValueError("Setiap elemen JSON harus berupa objek/dictionary.")

    return data


def proses_data(data: list[dict[str, Any]]) -> dict[str, Any]:
    # 1. LIST COMPREHENSION: mengambil nama semua data
    semua_nama = [item.get("nama", "Tanpa nama") for item in data]

    # 2. LIST COMPREHENSION: mengambil data dengan nilai >= 75
    nilai_lulus = [item for item in data
                   if isinstance(item.get("nilai"), (int, float))
                   and item["nilai"] >= 75]

    # 3. FILTER + LAMBDA: mengambil orang yang berumur >= 18 tahun
    dewasa = list(filter(
        lambda item: isinstance(item.get("umur"), (int, float))
        and item["umur"] >= 18,
        data
    ))

    # 4. FILTER + LAMBDA: mengambil data yang statusnya aktif
    data_aktif = list(filter(lambda item: item.get("aktif") is True, data))

    # 5. LIST COMPREHENSION: membuat daftar nama dan nilai
    ringkasan_nilai = [
        {"nama": item.get("nama", "Tanpa nama"), "nilai": item.get("nilai")}
        for item in data
    ]

    # 6. LIST COMPREHENSION: menambahkan status lulus/tidak lulus
    data_dengan_status = [
        {
            **item,
            "status_kelulusan": (
                "Lulus" if isinstance(item.get("nilai"), (int, float))
                and item["nilai"] >= 75 else "Tidak Lulus"
            )
        }
        for item in data
    ]

    return {
        "jumlah_data": len(data),
        "semua_nama": semua_nama,
        "nilai_minimal_75": nilai_lulus,
        "usia_minimal_18": dewasa,
        "data_aktif": data_aktif,
        "ringkasan_nilai": ringkasan_nilai,
        "data_dengan_status": data_dengan_status,
    }


def simpan_json(data: dict[str, Any], path: Path) -> None:
    """Menyimpan hasil pengolahan ke file JSON."""
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def main() -> None:
    print("=" * 50)
    print(" OPERASI PENGOLAHAN DATA JSON ")
    print(" LIST COMPREHENSION DAN FILTER LAMBDA ")
    print("=" * 50)

    data = baca_json(INPUT_JSON)
    hasil = proses_data(data)

    print(f"\nJumlah data       : {hasil['jumlah_data']}")
    print(f"Semua nama        : {hasil['semua_nama']}")
    print(f"Data nilai >= 75  : {[item.get('nama') for item in hasil['nilai_minimal_75']]}")
    print(f"Usia >= 18 tahun  : {[item.get('nama') for item in hasil['usia_minimal_18']]}")
    print(f"Data aktif        : {[item.get('nama') for item in hasil['data_aktif']]}")

    simpan_json(hasil, OUTPUT_JSON)
    print(f"\nHasil lengkap disimpan ke: {OUTPUT_JSON.resolve()}")
    print("Proses pengolahan JSON selesai.")


if __name__ == "__main__":
    main()
