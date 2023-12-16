import pandas as pd
import os
from pwinput import pwinput
import locale
import datetime

def tampilkanHeaderRegister():
    header = """\n\n
                                                                                _       _
                                                             _ __   ___   __ _ (_) ___ | |_   ___  _ __
                                                            | '__| / _ \\ / _` || |/ __|| __| / _ \\| '__|
                                                            | |   |  __/| (_| || |\\__ \\| |_ |  __/| |
                                                            |_|    \\___| \\__, ||_||___/ \\__| \\___||_|
                                                                         |___/ \n"""
    print(header)
def tampilkanHeaderLogin():
    header = """
                                                                 _                    _
                                                                | |      ___    __ _ (_) _ __
                                                                | |     / _ \\  / _` || || '_ \\
                                                                | |___ | (_) || (_| || || | | |
                                                                |_____| \\___/  \\__, ||_||_| |_|
                                                                               |___/            \n"""
    print(header)
def tampilkanHeader():
    header = """\n\n\n
                                                               _____  _  _    __  __
                                                              |  ___|(_)| |_ |  \\/  |  __ _  _ __
                                                              | |_   | || __|| |\\/| | / _` || '_ \\
                                                              |  _|  | || |_ | |  | || (_| || | | |
                                                              |_|    |_| \\__||_|  |_| \\__,_||_| |_|\n\n"""
    print(header)

def bersihkanLayar():
    os.system('cls' if os.name == 'nt' else 'clear')

def autentikasi():
    bersihkanLayar()
    while True:
        tampilkanHeader()
        print(f"{'1. Login / 2. Daftar / 3. Keluar':>95}")
        pilihan = input(f"{'Pilih [1/2/3]: ':>85}")
        
        if pilihan == '1':
            bersihkanLayar()
            info_pengguna = login()
            if info_pengguna:
                user, gender, berat, tinggi, umur, bmr, sisa_bmr, hari, kalolahraga = info_pengguna
                bersihkanLayar()
                menuUtama(user, gender, berat, tinggi, umur, bmr, sisa_bmr, hari, kalolahraga)
        elif pilihan == '2':
            bersihkanLayar()
            daftar()
        elif pilihan == '3':
            print('Terima kasih telah menggunakan aplikasi ini.')
            bersihkanLayar()
            break
        else:
            bersihkanLayar()
            print('Pilihan tidak valid. Silakan coba lagi.')
    return pilihan

def login():
    try:
        print('\n\n')
        tampilkanHeaderLogin()
        user = input(f"{'Username: ':>80}")
        password = pwinput(f"{'Password: ':>80}")
        if admin(user,password) == True:
            bersihkanLayar()
            menuAdmin()
        else:
            info_pengguna = periksaBiodataUser(user, password)
            bersihkanLayar()
            if info_pengguna:
                return info_pengguna
            else:
                print('Username atau password salah.')
                return None
    except:
        bersihkanLayar()
        print('belum ada database pada login')

def periksaBiodataUser(user, password):
    password = enkripsiPassword(password)
    df = pd.read_csv("data.csv")
    info_pengguna = df[df['user'] == user]
    
    if not info_pengguna.empty and info_pengguna.iloc[0]['password'] == password:
        return info_pengguna.iloc[0]['user'], info_pengguna.iloc[0]['gender'], info_pengguna.iloc[0]['berat'], info_pengguna.iloc[0]['tinggi'], info_pengguna.iloc[0]['umur'], info_pengguna.iloc[0]['BMR'], info_pengguna.iloc[0]['sisa_BMR'], info_pengguna.iloc[0]['hari'],info_pengguna.iloc[0]['olahraga']
    else:
        return None

def daftar():
    while True:
        try:
            tampilkanHeaderRegister()
            user = input(f"{'Username: ':>83}")
            if user == 'q':
                bersihkanLayar()
                return
            password = pwinput(f"{'Password: ':>83}")
            if password == 'q':
                bersihkanLayar()
                return
            if cekKeamananPass(password):
                berat = int(input(f"{'Berat (kg): ':>83}"))
                gender = input(f"{'Pria/Wanita: ':>83}")
                umur = int(input(f"{'Umur: ':>83}"))
                password = enkripsiPassword(password)
                if gender == 'pria' or 'p':
                    gender = 'pria'
                    tinggi = int(input(f"{'Tinggi Badan (cm): ':>83}"))
                    bmr = kalkulatorBmr(berat,tinggi,umur,gender)
                elif gender == 'wanita' or 'w':
                    gender = 'wanita'
                    tinggi = int(input(f"{'Tinggi Badan (cm): ':>83}"))
                    bmr = kalkulatorBmr(berat,tinggi,umur, gender)
                else:
                    print('Gender tidak valid.')
                    return
                if umur < 0 or berat < 0 or tinggi < 0:
                    bersihkanLayar()
                    print('maaf data yang anda input tidak valid')
                    return
                bersihkanLayar()
                periksaDanTambahkanUser(user, password, berat, gender, tinggi, umur, bmr)
                return
        except ValueError as e:
            bersihkanLayar()
            print('Input tidak valid. Silakan coba lagi.',e)
            return

def periksaDanTambahkanUser(user, password, berat, gender, tinggi, umur, bmr):
    hari = date.strftime('%A')
    try:
        membaca = pd.read_table("data.csv",sep=",")
        dataTertulis = pd.DataFrame(membaca)
        if user in dataTertulis['user'].values:
            bersihkanLayar()
            print('User sudah ada dalam database.')
        else:
            dataBaru = pd.DataFrame({
                'user': [user],
                'password': [password],
                'berat': [berat],
                'gender': [gender],
                'tinggi': [tinggi],
                'umur': [umur],
                'BMR': [bmr],
                'sisa_BMR': ['0'],
                'hari': [hari],
                'olahraga':['0']
            })
            dataGabung = pd.concat([dataTertulis, dataBaru], ignore_index=True)
            dataGabung.to_csv("data.csv", index=False,sep=',')
            print('User berhasil terdaftar. Silakan login.')
    except FileNotFoundError:
        dataBaru = pd.DataFrame({
            'user': [user],
            'password': [password],
            'berat': [berat],
            'gender': [gender],
            'tinggi': [tinggi],
            'umur': [umur],
            'BMR': [bmr],
            'sisa_BMR': ['0'],
            'hari':[hari],
            'olahraga':['0']
        })
        dataBaru.to_csv("data.csv", index=False,sep=',')
        print('User berhasil terdaftar. Silakan login.')

def menuUtama(user, gender, berat, tinggi, umur, bmr, sisaBmr, hari,kalOlahraga):
    simpanMakanan = []
    simpanKaloriMakan = []
    while True:
        bmr, sisaBmr, hari = reset(user,bmr,sisaBmr,hari)
        menu ="""                                       
                                                1. Pilih Makanan
                                                2. Pilih Olahraga
                                                3. Bantu Kami Menambahkan Menu Makanan
                                                4. Bantu Kami Menambahkan Pilihan Olahraga
                                                5. Logout
                                                6. Edit Profil
                                                7. Histori"""
        biodata = f"""
                                                ======================================================
                                                ||            Selamat datang di FitMan >:)          ||
                                                ======================================================

                                                =================== Profil Pengguna ==================
                                                                   Gender: {gender}                 
                                                                    Berat: {berat} KG               
                                                                   Tinggi: {tinggi} CM              
                                                                     Umur: {umur} tahun             
                                                       Kebutuhan Kalori Harian: {bmr} Kalori
                                                     kalori yang dibakar : {kalOlahraga} Kalori     
                                                ======================================================
        """
        biodata2 = f"""
                                                ======================================================
                                                ||            Selamat datang di FitMan >:)          ||
                                                ======================================================

                                                =================== Profil Pengguna ==================
                                                                   Gender: {gender}                 
                                                                    Berat: {berat} KG               
                                                                   Tinggi: {tinggi} CM              
                                                                     Umur: {umur} tahun
                                                    Kalori yang terpakai : {sisaBmr} kalori    
                                                        Sisa Kalori Harian: {bmr} Kalori   
                                                     kalori yang dibakar : {kalOlahraga} Kalori        
                                                ======================================================
        """
        if sisaBmr == 0:
            print(biodata)
        else:
            print(biodata2)
        print(f"{f'Halo {user} ! Silakan pilih menu.':>80}")
        print(menu)
        pilihan = input(f"\n{'Pilih menu: ':>63}")
        match pilihan:
            case '1':
                bersihkanLayar()
                bmr, sisaBmr, namaMakanan, kaloriMakanan = pilihMakanan(bmr, sisaBmr)
                simpanMakanan.append(namaMakanan)
                simpanKaloriMakan.append(kaloriMakanan)
                bersihkanLayar()
            case '2':
                bersihkanLayar()
                if int(sisaBmr) != 0:
                    kalOlahraga = pilihOlahraga(kalOlahraga,bmr)
                    bersihkanLayar()
                else:
                    bersihkanLayar()
                    print('makan dulu dong')
            case '3':
                bersihkanLayar()
                tambahMakandanOlahraga('makanan', 'dataMakan.csv', 'Nama', 'Kuantitas', 'Satuan', 'Kalori' )
            case '4':
                bersihkanLayar()
                tambahMakandanOlahraga('olahraga','Olahraga.csv','Jenis',"Durasi",'Waktu',"Kalori")
            case '5':
                bersihkanLayar()
                savehist = input('apakah anda ingin menyimpan data histori[Y/n]')
                if savehist in ['y','']:
                    simpanHistori(user,kalOlahraga,bmr,hari,simpanMakanan,simpanKaloriMakan)
                    simpanBmr(user,sisaBmr,bmr)
                    simpanKalOlahraga(user,kalOlahraga)
                print('Anda telah logout.')
                break
            case '6':
                bersihkanLayar()
                berat,tinggi,umur,menu,bmr = editProfil(user,berat,tinggi,umur,gender,bmr,sisaBmr)
                if menu == True:
                    return
            case '7':
                bersihkanLayar()
                histori(user,simpanMakanan,simpanKaloriMakan,bmr,kalOlahraga)
            case _:
                bersihkanLayar()
                print('Pilihan tidak valid. Silakan coba lagi.')

def pilihMakanan(bmr, sisaBmr):
    while True:
        try:
            batas = 25
            data = pd.read_csv("dataMakan.csv")
            jumlahBaris = data.shape[0]
            data.index += 1
            slice = int(jumlahBaris / batas)
            nomorMakanan = slicingMenu(data,0,0,batas,bmr,slice,jumlahBaris,'makanan')
            if nomorMakanan == 'q':
                return bmr, sisaBmr
            nomorMakanan = int(nomorMakanan)
            baris = data.loc[nomorMakanan]
            nama = str(baris.Nama)
            satuan = str(baris.Satuan)
            kuantitas = int(baris.Kuantitas)
            kalori = int(baris.Kalori)
            print(f'Anda makan {nama} dengan {kalori} kalori per {kuantitas} {satuan}')
            kalori /= kuantitas
            print('Satuan makanan yang dipilih:', satuan)
            porsi = input(f'Masukkan jumlah yang ingin Anda makan ({satuan}): ')
            if porsi == 'q':
                bersihkanLayar()
                print('silahkan memilih menu kembali')
            elif porsi <= 0:
                bersihkanLayar()
                print('maaf pilihan anda tidak valid')
            else:
                porsi = int(porsi)
                kalori *= porsi
                print(f'Anda mengonsumsi {kalori} kalori')
                kalori = int(kalori)
                if bmr > kalori:
                    bmr -= kalori
                    bmr = int(bmr)
                    sisaBmr += kalori
                    print('Kebutuhan kalori harian sekarang:', bmr)
                    input('\n\nTekan Enter untuk melanjutkan...')
                    return bmr, sisaBmr, nama, kalori
                else:
                    print("maaf kalori yang anda pilih melebihi bmr harian anda")
                    input('\n\nTekan Enter untuk melanjutkan...')
        except ValueError as e:
            bersihkanLayar()
            print('Input tidak valid. Silakan coba lagi.')
            #print(e)

def hapusAkun(user):
    df = pd.read_csv("data.csv")
    infoPengguna = df[df['user'] == user]
    
    if not infoPengguna.empty:
        df = df[df['user'] != user]
        df.to_csv('data.csv', index=False)
        print('Akun Anda telah dihapus.')
    else:
        print('Akun tidak ditemukan. Penghapusan gagal.')

def editProfil(user,berat,tinggi,umur,gender,bmr,sisaBmr):
    menu = False
    header = """\n\n
                                                            ===========================
                                                            ||       Edit Profil     ||
                                                            ===========================
    """
    menu ="""
                                                            1. Ganti berat badan
                                                            2. Ganti tinggi badan
                                                            3. Ganti Umur
                                                            4. Hapus akun
                                                            5. Kembali ke menu
    """
    while True:
        print(header)
        print(menu)
        pilihan = input(f"{'Masukkan nomor = ':>80}")
        match pilihan:
            case '1':
                berat = gantiBeratBadan(user,berat)
                bersihkanLayar()
                bmr = kalkulatorBmr(berat, tinggi, umur, gender)
                bmr -= sisaBmr
                UpdateUser('data',user,6,bmr)
                print('berat sudah diganti')
            case '2':
                tinggi = gantiTinggiBadan(user,tinggi)
                bersihkanLayar()
                bmr = kalkulatorBmr(berat, tinggi, umur, gender)
                bmr -= sisaBmr
                UpdateUser('data',user,6,bmr)
                print('tinggi sudah diganti')
            case '3':
                umur = gantiUmur(user,umur)
                bersihkanLayar()
                bmr = kalkulatorBmr(berat, tinggi, umur, gender)
                bmr -= sisaBmr
                UpdateUser('data',user,6,bmr)
                print('umur sudah diganti')
            case '4':
                print('Apakah Anda yakin? Jika ya, masukkan password Anda.')
                pw = pwinput('Masukkan Password: ')
                if periksaBiodataUser(user, pw):
                    bersihkanLayar()
                    hapusAkun(user)
                    menu = True
                    return None, None, None, menu, None
                else:
                    bersihkanLayar()
                    print('Password invalid')
            case '5':
                bersihkanLayar()
                return berat,tinggi,umur,menu,bmr

def simpanBmr(user, sisaBmr, bmr):
    df = pd.read_csv("data.csv")
    info_pengguna = df[df['user'] == user]
    if bmr != False:
        df.iloc[info_pengguna.index,6] = bmr
    if sisaBmr != False:
        df.iloc[info_pengguna.index,7] = sisaBmr
    df.to_csv('data.csv', index = False, sep=',')
    return

def simpanHistori(user,olahraga, bmr, hari,simpanMakanan,simpanKaloriMakan):
    olahraga += bmr
    try:
        df = pd.read_csv("histori.csv")
        if user in df['user'].values:
            infoPengguna = df[df['user'] == user]
            df.iloc[infoPengguna.index,1] = olahraga
            df.to_csv('histori.csv', index = False, sep=',')
            
        else:
            membaca = pd.read_table("histori.csv",sep=",")
            dataTertulis = pd.DataFrame(membaca)
            dataBaru = pd.DataFrame({
                'user': [user],
                'bmr': [olahraga],
                'hari':[hari]
            })
            dataGabung = pd.concat([dataTertulis, dataBaru], ignore_index=True)
            dataGabung.to_csv("histori.csv", index=False,sep=',')
            print('data sudah tersimpan pada histori')
    except FileNotFoundError:
        dataBaru = pd.DataFrame({
            'user': [user],
            'bmr': [olahraga],
            'hari':[hari]
        })
        dataBaru.to_csv("histori.csv", index=False,sep=',')
        print('data sudah tersimpan pada histori')

def cekKeamananPass(password):
    if ' ' in password:
        bersihkanLayar()
        print('Password tidak boleh memiliki spasi')
        return False

    if len(password) < 8:
        bersihkanLayar()
        print('Password minimal mempunyai panjang 8 karakter')
        return False

    return True


def pilihOlahraga(olahraga,bmr):
    while True:
        try:
            batas = 25
            data = pd.read_csv("Olahraga.csv")
            jumlahBaris = data.shape[0]
            data.index += 1
            slice = int(jumlahBaris / batas)
            nomorOlahraga = slicingMenu(data,0,0,batas,None,slice,jumlahBaris,'olahraga')
            if nomorOlahraga == 'q':
                return olahraga
            nomorOlahraga = int(nomorOlahraga)
            baris = data.loc[nomorOlahraga]
            waktu = str(baris.Waktu)
            durasi = int(baris.Durasi)
            kalori = int(baris.Kalori)
            print(f'Anda olahraga {baris.Jenis} dengan durasi {durasi} / {waktu} yang membakar {kalori} kalori')
            kalori /= durasi
            print('Olahraga yang anda dipilih:', baris.Jenis)
            total_waktu = int(input(f'Masukkan berapa {waktu} yang anda inginkan : '))
            kalori *= total_waktu
            if kalori < bmr / 1.5:
                print(f'Anda membakar {kalori} kalori')
                kalori = int(kalori)
                olahraga += kalori
                olahraga = int(olahraga)
                print('Kebutuhan kalori anda bertambah menjadi:', olahraga)
                input('\n\nTekan Enter untuk melanjutkan...')
                bersihkanLayar()
                return olahraga
            else:
                print('maaf, olahraga yang anda pilih melebihi batas olahraga harian')
                print('sebaiknya anda tidak lupa untuk beristirahat')
                input('\n\nTekan Enter untuk melanjutkan...')
                bersihkanLayar()
        except:
            bersihkanLayar()
            print('Input tidak valid. Silakan coba lagi.')

def tambahMakandanOlahraga(jenisPilihan,data,kolom1,kolom2,kolom3,kolom4):
    try:
        nama = input(f'Tulis {jenisPilihan} yang ingin ditambah = ').title()
        if jenisPilihan == 'makanan':
            satuan = input(f'{nama} memiliki satuan gram / porsi = ')
            if satuan == 'gram' or satuan == 'g':
                satuan = 'gram'
                kuantitas = int(input(f'Berapa {satuan} pada makanan tersebut = '))
            elif satuan == 'porsi' or satuan == 'p':
                satuan = 'porsi'
                kuantitas = int(input(f'Berapa {satuan} pada makanan tersebut = '))
            else :
                bersihkanLayar()
                print('maaf ada kesalahan input')
                return
        else:
            satuan = 'menit'
            kuantitas = int(input(f'Berapa {satuan} pada {jenisPilihan} tersebut = '))

        kalori = int(input(f'Masukkan berapa kalori pada {nama} = '))

    except:
        bersihkanLayar()
        print('maaf ada kesalahan input')
        return
    membaca = pd.read_table(f"{data}",sep=",")
    dataTertulis = pd.DataFrame(membaca)
    if nama in dataTertulis[f'{kolom1}'].values:
        bersihkanLayar()
        print(f'{nama} sudah ada dalam pilihan.')
        return
    else:
        dataBaru = pd.DataFrame({
            f'{kolom1}': [nama],
            f'{kolom2}': [kuantitas],
            f'{kolom3}': [satuan],
            f'{kolom4}': [kalori]
        })
        dataGabung = pd.concat([dataTertulis, dataBaru], ignore_index=True)
        dataGabung.to_csv(f"{data}", index=False,sep=',')
        urutkanCsv(data,kolom1)
        print("Data makanan telah disimpan")
        input('klik enter untuk kembali..')
        bersihkanLayar()
        return

def urutkanCsv(data,kolom1):
    df = pd.read_csv(f'{data}')
    df = df.sort_values(by=f'{kolom1}')
    df.to_csv(f'{data}', index=False)
    return

def gantiBeratBadan(user,berat):
    df = pd.read_csv("data.csv")
    berat = int(input('Masukkan Berat Terbaru = '))
    info_pengguna = df[df['user'] == user]
    df.iloc[info_pengguna.index,2] = berat
    df.to_csv('data.csv', index = False, sep=',')
    return berat

def gantiTinggiBadan(user,tinggi):
    df = pd.read_csv("data.csv")
    tinggi = int(input('Masukkan Tinggi Terbaru = '))
    infoPengguna = df[df['user'] == user]
    df.iloc[infoPengguna.index,4] = tinggi
    df.to_csv('data.csv', index = False, sep=',')
    return tinggi

def gantiUmur(user,umur):
    df = pd.read_csv("data.csv")
    umur = int(input('Masukkan umur Terbaru = '))
    infoPengguna = df[df['user'] == user]
    df.iloc[infoPengguna.index,5] = umur
    df.to_csv('data.csv', index = False, sep=',')
    return umur

def enkripsiPassword(password):
    tampung = ""
    for huruf in password:
        ganti = ord(huruf)
        ganti += 3
        huruf = chr(ganti)
        tampung += huruf
    return tampung

def dekripsiPassword(password):
    tampung = ""
    for huruf in password:
        ganti = ord(huruf)
        ganti -= 3
        huruf = chr(ganti)
        tampung += huruf
    return tampung

def histori(user,simpanMakanan,simpanKaloriMakan,bmr,kalOlahraga):
    print('1. Data Sekarang')
    print('2. Histori yang anda simpan')
    pilihan = input('Pilih Menu (tekan q untuk kembali): ')
    bersihkanLayar()
    if pilihan == '1': 
        df = pd.read_csv('histori.csv')
        ambil = df[df['user'] == user]
        if not simpanMakanan == []:
            print(f'data dan sisa BMR anda sekarang = {bmr + kalOlahraga}')
            for i in range(len(simpanMakanan)):
                print(simpanMakanan[i],'=', + simpanKaloriMakan[i])
                input('Tekan Enter untuk kembali...')
        else:
            print('Anda belum memiliki histori')
            input('Klik Enter untuk kembali...')
    elif pilihan == '2':
        df = pd.read_csv('histori.csv')
        ambil = df[df['user'] == user]
        if not ambil.empty:
            print(f'selamat! sisa BMR anda pada hari {ambil.hari.values[0]} = {ambil.bmr.values[0]}')
            input('Tekan Enter untuk kembali...')
        else : 
            print(f'Data Anda Kemarin Belum Ada')
            input('Tekan Enter Untuk Kembali...')
    elif pilihan == 'q':
        return

def admin(user, password):
    if user == 'admin' and password == "admin":
        return True
    
def menuAdmin():
    headerAdmin = """
    1. Hapus Makanan
    2. hapus Olahraga
    3. Hapus user akun
    4. Reset user akun
    5. Keluar"""
    print(headerAdmin)
    pilihan = input('masukkan nomor = ')
    match pilihan:
        case '1':
            hapusMakanan()
        case '2':
            hapusOlahraga()
        case '3':
            user = input('masukkan nama user = ')
            hapusAkun(user)
        case '4':
            user = input('masukkan nama user = ')
            df = pd.read_csv("data.csv")
            info_pengguna = df[df['user'] == user]
            bmr, sisaBmr = info_pengguna.iloc[0]['BMR'],info_pengguna.iloc[0]['sisa_BMR']
            reset(user,bmr,sisaBmr,'admin')
        case '5':
            return
            

def slicingMenu(data, i, start, batas, bmr,slice,jumlahBaris,jenis):
    while True:
        print(data.iloc[start:batas])
        print("\n" + "-"*80 + "\n")
        if jenis == 'makanan':
            print(f'Kebutuhan kalori harian Anda: {bmr} Kalori')
        elif jenis == 'admin':
            print('anda berada di akun admin')
        nomorMakanan = input('Pilih nomor item makanan, (lanjut/kembali [Y/n] tekan "q" untuk keluar): ')
        if nomorMakanan == 'q':
            return nomorMakanan
        elif nomorMakanan.lower() in ['y','']:
            if i != slice:
                start += 25
                batas += 25
                i += 1
                bersihkanLayar()
            else:
                start += 0
                batas = jumlahBaris
                bersihkanLayar()
        elif nomorMakanan.lower() == 'n':
            if i != 0:
                start -= 25
                batas -= 25
                i -= 1
                bersihkanLayar()
        else:
            return nomorMakanan

def kalkulatorBmr(berat,tinggi,umur,gender):
    if gender == 'wanita':
        bmr = int((10 * berat) + (6.25 * tinggi) - (5 * umur) - 161)
    else:
        bmr = int((10 * berat) + (6.25 * tinggi) - (5 * umur) + 5)
    return bmr

def UpdateUser(namaCsv,user,nomor,yangInginDiganti):
    df = pd.read_csv(f"{namaCsv}.csv")
    infoPengguna = df[df['user'] == user]
    df.iloc[infoPengguna.index,nomor] = yangInginDiganti
    df.to_csv(f'{namaCsv}.csv', index = False, sep=',')

def reset(user, bmr, sisaBmr, hari):
    hariSekarang = date.strftime('%A')
    if hari != hariSekarang or hari == 'admin':
        bmr += sisaBmr
        sisaBmr = 0
        print('selamat datang kembali, biodata anda sudah di reset')
        UpdateUser('data',user,6,bmr)
        UpdateUser('data',user,7,sisaBmr)
        UpdateUser('data',user,8,hariSekarang)
        return bmr,sisaBmr, hariSekarang
    return bmr, sisaBmr, hariSekarang

def hapusMakanan():
    while True:
        try:
            batas = 25
            df = pd.read_csv("dataMakan.csv")
            jumlahBaris = df.shape[0]
            df.index += 1
            slice = int(jumlahBaris / batas)
            nomorMakanan = int(slicingMenu(df,0,0,batas,None,slice,jumlahBaris,'admin'))
            nomorMakanan -= 1
            baris = df.iloc[nomorMakanan,0]
            print(baris)
            infoMakanan = df[df['Nama'] == baris]
            if not infoMakanan.empty:
                df = df[df['Nama'] != baris]
                df.to_csv('dataMakan.csv', index=False)
                print('Makanan telah dihapus.')
            else:
                print('Makanan tidak ditemukan. Penghapusan gagal.')
        except Exception as e:
            print(e)

def hapusOlahraga():
    while True:
        try:
            batas = 25
            df = pd.read_csv("dataOlahraga.csv")
            jumlahBaris = df.shape[0]
            df.index += 1
            slice = int(jumlahBaris / batas)
            nomorMakanan = int(slicingMenu(df,0,0,batas,None,slice,jumlahBaris,'admin'))
            nomorMakanan -= 1
            baris = df.iloc[nomorMakanan,0]
            print(baris)
            infoMakanan = df[df['Jenis'] == baris]
            if not infoMakanan.empty:
                df = df[df['Jenis'] != baris]
                df.to_csv('dataOlahraga.csv', index=False)
                print('Makanan telah dihapus.')
            else:
                print('Makanan tidak ditemukan. Penghapusan gagal.')
        except Exception as e:
            print(e)

def simpanKalOlahraga(user,kalOlahraga):
    UpdateUser('data',user,9,kalOlahraga)


locale.setlocale(locale.LC_TIME, 'id_ID')
date = datetime.datetime.now()
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

while True:
    bersihkanLayar()
    try:
        pilihan = autentikasi()
        if pilihan == '3':
            break
    except KeyboardInterrupt:
        print('Aplikasi sedang ditutup.')
        break
