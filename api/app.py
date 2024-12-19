from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Basis pengetahuan (diperbarui dengan data baru)
basis_pengetahuan = [
    {"Nama": "Lumba-lumba Hidung Botol", "Klasifikasi": "Mamalia", "Habitat": "Pantai dan Lautan", "Jenis_Makanan": "Plankton dan Ikan", "Ciri_Bentuk_Tubuh": "Lonjong", "Tingkah_Laku": "Nocturnal", "Warna_Tubuh": "Abu-abu keputihan", "Tempat_Tinggal": "Air"},
    {"Nama": "Harimau Sumatera", "Klasifikasi": "Mamalia", "Habitat": "Hutan Hujan Besar", "Jenis_Makanan": "Karnivora", "Ciri_Bentuk_Tubuh": "Berat dengan Cakar Besar", "Tingkah_Laku": "Soliter", "Warna_Tubuh": "Orange dengan Garis Tiger", "Tempat_Tinggal": "Darat"},
    {"Nama": "Gajah Asia", "Klasifikasi": "Mamalia", "Habitat": "Hutan dan Padang Savana", "Jenis_Makanan": "Herbivora", "Ciri_Bentuk_Tubuh": "Besar dengan Belalai", "Tingkah_Laku": "Kepekaan Gerakan Tinggi", "Warna_Tubuh": "Abu-abu", "Tempat_Tinggal": "Darat"},
    {"Nama": "Orangutan", "Klasifikasi": "Mamalia", "Habitat": "Hutan Hujan", "Jenis_Makanan": "Omnivora", "Ciri_Bentuk_Tubuh": "Kekar dengan Tangan Panjang", "Tingkah_Laku": "Soliter", "Warna_Tubuh": "Orange dengan Rambut Panjang", "Tempat_Tinggal": "Darat"},
    {"Nama": "Kelelawar Buah", "Klasifikasi": "Mamalia", "Habitat": "Hutan dan Area Terbuka", "Jenis_Makanan": "Frugivora", "Ciri_Bentuk_Tubuh": "Berbulu", "Tingkah_Laku": "Nocturnal", "Warna_Tubuh": "Hitam dengan Bercak Kuning", "Tempat_Tinggal": "Darat"},
    {"Nama": "Badak Jawa", "Klasifikasi": "Mamalia", "Habitat": "Hutan Bakau dan Hutan", "Jenis_Makanan": "Herbivora", "Ciri_Bentuk_Tubuh": "Besar dengan Kulit Kasar", "Tingkah_Laku": "Soliter", "Warna_Tubuh": "Abu-abu Kelabu", "Tempat_Tinggal": "Darat"},
    {"Nama": "Beruang Madu", "Klasifikasi": "Mamalia", "Habitat": "Hutan Hujan", "Jenis_Makanan": "Omnivora", "Ciri_Bentuk_Tubuh": "Tegap dengan Cakar Panjang", "Tingkah_Laku": "Soliter", "Warna_Tubuh": "Hitam dengan Cincin Kuning", "Tempat_Tinggal": "Darat"},
    {"Nama": "Rusa Timor", "Klasifikasi": "Mamalia", "Habitat": "Hutan dan Padang Rumput", "Jenis_Makanan": "Herbivora", "Ciri_Bentuk_Tubuh": "Cepat dengan Tanduk", "Tingkah_Laku": "Nocturnal", "Warna_Tubuh": "Coklat Pudar dengan Putih di Perut", "Tempat_Tinggal": "Darat"},
    {"Nama": "Trenggiling Jawa", "Klasifikasi": "Mamalia", "Habitat": "Hutan dan Area Terbuka", "Jenis_Makanan": "Insektofag", "Ciri_Bentuk_Tubuh": "Kecil dengan Bulu Perisai", "Tingkah_Laku": "Nocturnal", "Warna_Tubuh": "Berlian Coklat", "Tempat_Tinggal": "Darat"},
    {"Nama": "Kuskus", "Klasifikasi": "Mamalia", "Habitat": "Hutan dan Area Bervegetasi", "Jenis_Makanan": "Herbivora", "Ciri_Bentuk_Tubuh": "Kecil dengan Ekor Panjang", "Tingkah_Laku": "Soliter", "Warna_Tubuh": "Abu-abu Coklat", "Tempat_Tinggal": "Darat"}
]

# Helper function untuk mencocokkan fakta dengan probabilitas
def match_facts(input_facts, mamalia):
    matched_attributes = []
    score = 0

    for key, value in input_facts.items():
        if mamalia.get(key) == value:
            matched_attributes.append(key)
            score += 1

    total_attributes = len(input_facts)
    probability = (score / total_attributes) if total_attributes > 0 else 0
    return matched_attributes, probability

# Forward chaining
def forward_chaining(input_facts):
    matched_results = []
    for mamalia in basis_pengetahuan:
        matched_attributes, probability = match_facts(input_facts, mamalia)
        if probability > 0.3:  # Threshold 30%
            matched_results.append({
                "Nama": mamalia["Nama"],
                "Klasifikasi": mamalia["Klasifikasi"],
                "Probability": f"{probability * 100:.2f}%",
                "Matched_Attributes": matched_attributes
            })
    return matched_results

# Endpoint untuk mencari mamalia berdasarkan fakta
@app.route('/cari-mamalia', methods=['POST'])
def cari_mamalia():
    # Validasi method
    if request.method != 'POST':
        return jsonify({
            "error": "Method Not Allowed",
            "message": "Silakan gunakan Postman atau aplikasi lain untuk mengakses endpoint ini dengan method POST."
        }), 405

    input_facts = request.json

    # Validasi input
    if not input_facts:
        return jsonify({
            "error": "Data input tidak boleh kosong",
            "required_fields": ["Habitat", "Jenis_Makanan", "Ciri_Bentuk_Tubuh", "Tingkah_Laku", "Warna_Tubuh", "Tempat_Tinggal"]
        }), 400

    results = forward_chaining(input_facts)

    if not results:
        return jsonify({"message": "Tidak ditemukan mamalia yang cocok dengan fakta yang diberikan."}), 404

    return jsonify({"results": results})

# Endpoint untuk mendapatkan daftar nilai yang mungkin untuk setiap atribut
@app.route('/get-options', methods=['GET'])
def get_options():
    options = {
        "Habitat": list(set(m["Habitat"] for m in basis_pengetahuan)),
        "Jenis_Makanan": list(set(m["Jenis_Makanan"] for m in basis_pengetahuan)),
        "Ciri_Bentuk_Tubuh": list(set(m["Ciri_Bentuk_Tubuh"] for m in basis_pengetahuan)),
        "Tingkah_Laku": list(set(m["Tingkah_Laku"] for m in basis_pengetahuan)),
        "Warna_Tubuh": list(set(m["Warna_Tubuh"] for m in basis_pengetahuan)),
        "Tempat_Tinggal": list(set(m["Tempat_Tinggal"] for m in basis_pengetahuan))
    }
    return jsonify(options)

# Endpoint default (root) untuk memberikan informasi
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "Selamat datang di API Sistem Pakar Mamalia!",
        "endpoints": {
            "/cari-mamalia (POST)": "Cari mamalia berdasarkan fakta yang diberikan",
            "/get-options (GET)": "Dapatkan daftar nilai yang mungkin untuk setiap atribut"
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
