import subprocess
import os

def clear_screen():
    """Ekranı temizle"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Başlık yazdır"""
    print("=" * 50)
    print("                CHAMPZ BOT")
    print("=" * 50)
    print()

def print_menu():
    """Ana menüyü yazdır"""
    print("1. Botu Başlat")
    print("2. Bearer Token Güncelle")
    print("3. Karakterleri Oluştur")
    print("4. Item Giydir")
    print("5. Daily Claim")
    print("6. Chest Aç")
    print("7. Quest")
    print("8. Burn")
    print("9. Çıkış")

    print("\nSeçiminiz (1-7): ", end="")

def run_bot():
    """Botu başlat"""
    print("Bot başlatılıyor...")
    subprocess.run(["python", "function/bot.py"])  # function/bot.py dosyasını çalıştır

def run_brear_update():
    """Brear token güncelleme işlemini başlat"""
    print("Brear token güncelleniyor...")
    subprocess.run(["python", "function/brear.py"])  # function/brear.py dosyasını çalıştır

def run_character_creation():
    """Karakter oluşturma işlemini başlat"""
    print("Karakter oluşturma işlemi başlatılıyor...")
    subprocess.run(["python", "function/karakter.py"])  # function/karakter.py dosyasını çalıştır

def run_item_giydir():
    """Item giydirme işlemini başlat"""
    print("Item giydirme işlemi başlatılıyor...")
    subprocess.run(["python", "function/itemgiy.py"])  # function/itemgiy.py dosyasını çalıştır

def run_quest():
    """QUEST işlemini başlat"""
    print("Quest işlemi başlatılıyor...")
    subprocess.run(["python", "function/quest.py"]) 
def run_burn():
    """BURN işlemini başlat"""
    print("BURN işlemi başlatılıyor...")
    subprocess.run(["python", "function/burn.py"]) 

def main():
    clear_screen()
    print_header()

    while True:
        print_menu()
        choice = input().strip()

        if choice == "1":
            run_bot()  # Botu başlat

        elif choice == "2":
            run_brear_update()  # Brear token güncelleme işlemini başlat

        elif choice == "3":
            run_character_creation()  # Karakter oluşturma işlemini başlat

        elif choice == "4":
            run_item_giydir()  # Item giydirme işlemini başlat

        elif choice == "5":
            print("Daily Claim işlemi başlatılıyor...")
            subprocess.run(["python", "function/dailylogin.py"])  # function/dailylogin.py dosyasını çalıştır

        elif choice == "6":
            print("Chest açma işlemi başlatılıyor...")
            subprocess.run(["python", "function/chestac.py"])  # function/chestac.py dosyasını çalıştır
        elif choice == "7":
            print("Chest açma işlemi başlatılıyor...")
            subprocess.run(["python", "function/quest.py"]) 
        elif choice == "8":
            print("burn açma işlemi başlatılıyor...")
            subprocess.run(["python", "function/burn.py"])  # function/chestac.py dosyasını çalıştır
        elif choice == "9":
            clear_screen()
            print_header()
            print("Programdan çıkılıyor...")
            break

        else:
            input("\nGeçersiz seçim! Devam etmek için Enter'a basın...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print_header()
        print("Program sonlandırıldı.")
