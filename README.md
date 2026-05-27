# Algoritma Genetika - Knapsack Problem

| Informasi | Detail |
|-----------|--------|
| **Nama** | Yosi Rahmawati |
| **NIM** | H1D024019 |
| **Shift KRS** | G |
| **Shift Baru** | F |

---

## Deskripsi

Program ini adalah implementasi **Algoritma Genetika (Genetic Algorithm)** dalam Python untuk menyelesaikan **Knapsack Problem** (masalah pengisian tas). Program mencari kombinasi barang terbaik yang dapat dimasukkan ke dalam tas dengan kapasitas terbatas, dengan tujuan memaksimalkan total nilai barang yang dipilih.

---

## Struktur File

```
prakKB9/
│
├── inisiasipopulasi.py   # Membangkitkan populasi awal secara acak
├── evaluasifitness.py    # Menghitung nilai fitness setiap individu
├── selection.py          # Proses seleksi orang tua
├── crossover.py          # Proses penyilangan kromosom
├── mutation.py           # Proses mutasi kromosom
└── main.py               # Program utama yang menjalankan seluruh proses GA
```

---

## Cara Menjalankan

Install library yang dibutuhkan terlebih dahulu:
```bash
pip install matplotlib numpy
```

Jalankan program utama:
```bash
python main.py
```

Jalankan file per bagian untuk melihat output masing-masing proses:
```bash
python inisiasipopulasi.py
python evaluasifitness.py
python selection.py
python crossover.py
python mutation.py
```

---

## Data Barang

Program menggunakan 9 barang dengan nilai dan berat sebagai berikut:

| Barang   | Nilai | Berat |
|----------|-------|-------|
| Barang1  | 60    | 10    |
| Barang2  | 100   | 20    |
| Barang3  | 120   | 30    |
| Barang4  | 90    | 25    |
| Barang5  | 69    | 11    |
| Barang6  | 70    | 9     |
| Barang7  | 80    | 15    |
| Barang8  | 90    | 10    |
| Barang9  | 25    | 3     |

**Kapasitas Tas:** 50

---

## Penjelasan Source Code Per Bagian

---

### 1. `inisiasipopulasi.py` - Inisialisasi Populasi Awal

```python
def inisialisasi_populasi(jumlah_populasi, jumlah_gen):
    populasi = []
    for i in range(jumlah_populasi):
        kromosom = [random.randint(0, 1) for _ in range(jumlah_gen)]
        populasi.append(kromosom)
    return populasi
```

**Penjelasan:**
Fungsi ini bertugas membangkitkan populasi awal yang terdiri dari sejumlah kromosom secara acak. Setiap kromosom merupakan representasi biner dari solusi potensial, di mana:
- `1` berarti barang tersebut **dipilih** untuk dimasukkan ke dalam tas
- `0` berarti barang tersebut **tidak dipilih**

**Kegunaan:**
Populasi awal ini menjadi titik awal dari proses evolusi. Setiap individu (kromosom) merepresentasikan satu kemungkinan kombinasi barang yang akan dioptimasi oleh algoritma genetika dari generasi ke generasi.

**Contoh Output:**
```
Populasi Awal:
Individu 1: [1, 0, 1, 0, 0, 1, 0, 1, 0]
Individu 2: [0, 1, 0, 1, 1, 0, 0, 1, 1]
...
```

---

### 2. `evaluasifitness.py` - Evaluasi Nilai Fitness

```python
def hitung_fitness(kromosom, barang, kapasitas_tas):
    total_harga = 0
    total_bobot = 0
    for i in range(len(kromosom)):
        if kromosom[i] == 1:
            total_harga += barang[i][1]
            total_bobot += barang[i][2]
    if total_bobot > kapasitas_tas:
        return 0
    else:
        return total_harga
```

**Penjelasan:**
Fungsi ini menghitung nilai fitness dari setiap kromosom. Proses perhitungannya adalah sebagai berikut:
1. Setiap gen diperiksa satu per satu
2. Jika gen bernilai `1`, harga dan berat barang yang bersangkutan dijumlahkan
3. Jika total berat **melebihi kapasitas tas**, nilai fitness di-set menjadi `0` sebagai penalti (solusi tidak valid)
4. Jika total berat masih dalam batas kapasitas, nilai fitness = total harga barang yang dipilih

**Kegunaan:**
Nilai fitness digunakan sebagai tolak ukur seberapa baik suatu individu dalam memecahkan masalah. Individu dengan nilai fitness tinggi menunjukkan kombinasi barang yang optimal — nilai besar namun berat tetap dalam batas kapasitas.

**Contoh Output:**
```
Nilai Fitness:
Individu 1: Fitness = 0
Individu 2: Fitness = 190
Individu 3: Fitness = 230
```

---

### 3. `selection.py` - Proses Seleksi Orang Tua

Terdapat dua metode seleksi yang diimplementasikan:

#### Roulette Wheel Selection
```python
def roulette_wheel_selection(populasi, fitness_populasi):
    probabilitas = [fitness / total_fitness for fitness in fitness_populasi]
    ...
    for i, kum_prob in enumerate(kumulatif_prob):
        if r <= kum_prob:
            return populasi[i], i
```

**Penjelasan:**
Setiap individu mendapatkan probabilitas seleksi yang sebanding dengan nilai fitness-nya terhadap total fitness seluruh populasi. Individu dengan fitness tinggi memiliki peluang lebih besar untuk terpilih, namun individu dengan fitness rendah tetap memiliki peluang untuk dipilih.

**Kegunaan:**
Metode ini memastikan bahwa individu-individu dengan solusi yang lebih baik memiliki kontribusi lebih besar dalam membentuk generasi berikutnya, sambil tetap menjaga keberagaman populasi.

#### Tournament Selection
```python
def tournament_selection(populasi, fitness_populasi, k=3):
    peserta_indices = random.sample(range(len(populasi)), k)
    peserta.sort(key=lambda x: x[1], reverse=True)
    return peserta[0][0], peserta[0][2]
```

**Penjelasan:**
Sejumlah `k` individu dipilih secara acak dari populasi untuk mengikuti turnamen. Dari peserta turnamen tersebut, individu dengan nilai fitness tertinggi yang akan menjadi orang tua.

**Kegunaan:**
Memberikan tekanan seleksi yang dapat dikontrol melalui ukuran turnamen `k`. Semakin besar `k`, semakin besar kemungkinan individu terbaik terpilih.

**Contoh Output:**
```
Parent Terpilih:
Parent 1: individu4
Parent 2: individu3
```

---

### 4. `crossover.py` - Proses Penyilangan (Crossover)

Terdapat tiga metode crossover yang diimplementasikan:

#### One-Point Crossover *(digunakan di `main.py`)*
```python
def one_point_crossover(parent1, parent2):
    titik_potong = random.randint(1, len(parent1)-1)
    anak1 = parent1[:titik_potong] + parent2[titik_potong:]
    anak2 = parent2[:titik_potong] + parent1[titik_potong:]
    return anak1, anak2
```

**Penjelasan:**
Dua kromosom orang tua dipotong di satu titik acak, kemudian bagian-bagiannya ditukar untuk menghasilkan dua kromosom anak baru.

```
Parent 1:  [1, 0, 1 | 1, 0]
Parent 2:  [0, 1, 0 | 0, 1]
                  titik potong ke-3
Anak 1:    [1, 0, 1, 0, 1]
Anak 2:    [0, 1, 0, 1, 0]
```

#### Two-Point Crossover

**Penjelasan:**
Sama seperti one-point crossover, namun pemotongan kromosom dilakukan di dua titik, sehingga segmen tengah dari masing-masing orang tua yang ditukar.

#### Uniform Crossover

**Penjelasan:**
Setiap gen pada kromosom anak ditentukan berdasarkan pola masking acak (0 atau 1). Jika mask bernilai `0`, gen diambil dari parent1; jika mask bernilai `1`, gen diambil dari parent2.

**Kegunaan:**
Crossover bertujuan menghasilkan individu baru dengan mengombinasikan informasi genetik dari dua orang tua, dengan harapan menghasilkan keturunan yang memiliki sifat-sifat terbaik dari keduanya.

**Contoh Output:**
```
Anak Hasil Crossover:
Anak 1: [1, 0, 1, 0, 1]
Anak 2: [0, 1, 0, 1, 0]
```

---

### 5. `mutation.py` - Proses Mutasi

Terdapat tiga metode mutasi yang diimplementasikan:

#### Swap Mutation *(digunakan di `main.py`)*
```python
def swap_mutation(kromosom):
    posisi1, posisi2 = random.sample(range(len(kromosom)), 2)
    kromosom[posisi1], kromosom[posisi2] = kromosom[posisi2], kromosom[posisi1]
    return kromosom
```

**Penjelasan:**
Dua posisi gen dipilih secara acak, kemudian nilainya ditukar satu sama lain.

#### Inversion Mutation

**Penjelasan:**
Dua posisi dipilih secara acak, kemudian urutan gen di antara kedua posisi tersebut dibalik.

#### Uniform Mutation

**Penjelasan:**
Setiap gen memiliki peluang kecil (`mutation_rate = 0.1`) untuk dibalik nilainya dari `0` menjadi `1` atau sebaliknya.

**Kegunaan:**
Mutasi berfungsi menjaga keberagaman genetik dalam populasi dan mencegah algoritma terjebak pada solusi lokal yang tidak optimal. Tanpa mutasi, algoritma bisa berhenti berkembang karena variasi antar individu menjadi terlalu kecil.

**Contoh Output:**
```
Anak Setelah Mutasi:
Anak 1 (Swap Mutation):      [1, 1, 1, 0, 0]
Anak 2 (Inversion Mutation): [0, 1, 1, 0, 1]
Anak 3 (Uniform Mutation):   [0, 1, 1, 0, 1]
```

---

### 6. `main.py` - Program Utama

```python
run_ga(
    jumlah_generasi=50,
    jumlah_populasi=20,
    prob_crossover=0.5,
    prob_mutasi=0.1,
    kapasitas_tas=50
)
```

**Penjelasan:**
File ini adalah pusat dari seluruh program. Semua fungsi dari file lain diimport dan dirangkai menjadi satu alur kerja Algoritma Genetika yang utuh.

**Alur kerja di dalam `run_ga()`:**

```
[1] Buat populasi awal (20 individu, 9 gen)
        |
[2] Ulangi proses berikut sebanyak 50 generasi:
    |-- [a] Hitung fitness semua individu
    |-- [b] Simpan nilai fitness terbaik, terburuk, rata-rata
    |-- [c] Seleksi dua orang tua (Roulette Wheel Selection)
    |-- [d] Crossover -> hasilkan 2 anak baru (One-Point, prob. 50%)
    |-- [e] Mutasi pada anak (Swap Mutation, prob. 10%)
    |-- [f] Anak-anak menjadi populasi generasi berikutnya
        |
[3] Tampilkan hasil terbaik dan grafik perkembangan fitness
```

**Parameter yang dapat diubah:**

| Parameter         | Nilai | Keterangan                                     |
|-------------------|-------|------------------------------------------------|
| `jumlah_generasi` | 50    | Jumlah iterasi evolusi yang dijalankan         |
| `jumlah_populasi` | 20    | Jumlah individu dalam satu generasi            |
| `prob_crossover`  | 0.5   | Probabilitas terjadinya crossover (50%)        |
| `prob_mutasi`     | 0.1   | Probabilitas terjadinya mutasi pada anak (10%) |
| `kapasitas_tas`   | 50    | Batas maksimum berat yang dapat ditampung tas  |

---

## Output Program

### Terminal
```
Nilai Fitness Terbaik: 329
Total Bobot: 50
Barang Terpilih:
- Barang2
- Barang5
- Barang6
- Barang8
```

### Grafik Perkembangan Fitness

Program menampilkan grafik perkembangan nilai fitness selama 50 generasi dengan keterangan warna:

| Warna  | Keterangan                              |
|--------|-----------------------------------------|
| Biru   | Nilai fitness tertinggi per generasi    |
| Kuning | Nilai fitness terendah per generasi     |
| Merah  | Rata-rata nilai fitness per generasi    |
| Abu-abu | Sebaran nilai fitness seluruh individu |

---

## Mengapa Hasilnya Berbeda Setiap Dijalankan?

Algoritma Genetika bersifat **stokastik** — ada proses acak pada setiap tahapnya mulai dari pembangkitan populasi awal, seleksi orang tua, crossover, hingga mutasi. Akibatnya, setiap kali program dijalankan, alur evolusi yang terjadi bisa berbeda dan menghasilkan solusi yang sedikit bervariasi.

Untuk mendapatkan hasil yang konsisten, tambahkan baris berikut di bagian awal `main.py`:
```python
random.seed(42)  # Angka seed dapat diubah sesuai kebutuhan
```
