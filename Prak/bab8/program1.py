class Orang:
    total = 0

    def __init__(self, nama):
        self.nama = nama
        self.fav_game = []
        Orang.total += 1

    def __del__(self):
        print("Data dari %s, Telah dihapus" %self.nama)
        Orang.total -= 1
    
    def add_favgame(self,game):
        self.fav_game.append(game)

    def remove_favgame(self,game):
        self.fav_game.remove(game)
    
    def edit_favgame(self,game,ke):
        self.fav_game[ke] = game

    def katakanHalo(self):
        print('Halo, nama saya %s, apa kabar?' % self.nama)

    def total_populasi(self):
        print('Total Orang %s' % self.total)

    def tampil_Profile(self):
        print("Nama: %s"%self.nama)
        print("Memiliki Game Kesukaan:")
        for i in self.fav_game:
            print(i)

    total_populasi = classmethod(total_populasi)


org = Orang('Sukijan')
org.add_favgame("Dota2")
org.add_favgame("Nikke")
org.add_favgame("Subwaysurf")
org.katakanHalo()
org.total_populasi()
org.tampil_Profile()
org.edit_favgame("Genshin",2)
org.tampil_Profile()
org.remove_favgame("Genshin")
org2 = Orang('Azizoy')
org2.add_favgame("GrandChase")
org2.katakanHalo()
org.total_populasi()
Orang.total_populasi()