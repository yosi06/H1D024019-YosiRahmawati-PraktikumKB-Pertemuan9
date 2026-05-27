import random

def inisialisasi_populasi(jumlah_populasi, jumlah_gen):
    populasi = []
    for i in range(jumlah_populasi):
        kromosom = [random.randint(0, 1) for _ in range(jumlah_gen)]
        populasi.append(kromosom)
    return populasi

if __name__ == '__main__':
    jumlah_populasi = 10
    jumlah_gen = 5
    populasi_awal = inisialisasi_populasi(jumlah_populasi, jumlah_gen)
    print("Populasi Awal:")
    for idx, individu in enumerate(populasi_awal):
        print(f"Individu {idx+1}: {individu}")
