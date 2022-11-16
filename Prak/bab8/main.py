class Karyawan:
    jumlah_karyawan = 0

    def __init__(self, nama, gaji):
        self.nama = nama
        self.gaji = gaji
        Karyawan.jumlah_karyawan += 100

    def tampilkan_jumlah(self):
        print("Total karyawan:", Karyawan.jumlah_karyawan)

    def tampilkan_profil(self):
        print("Nama:", self.nama, "\nGaji:", self.gaji, "\n")

    tampilkan_jumlah = classmethod(tampilkan_jumlah)


karyawan1 = Karyawan("Sarah", 1000000)
karyawan2 = Karyawan("Budi", 2000000)

print(karyawan1, karyawan2)
karyawan1.tampilkan_profil()
karyawan2.tampilkan_profil()

karyawan1.tampilkan_jumlah()
karyawan2.tampilkan_jumlah()