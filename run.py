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
    print("2. Brear Token Güncelle")
    print("3. Karakterleri Oluştur")
    print("4. Item Giydir")
    print("5. Çıkış")
    print("\nSeçiminiz (1-5): ", end="")

def run_bot():
    """Botu başlat"""
    print("Bot başlatılıyor...")
    subprocess.run(["python", "bot.py"])  # bot.py dosyasını çalıştır

def run_character_creation():
    """Karakter oluşturma işlemini başlat"""
    print("Karakter oluşturma işlemi başlatılıyor...")
    subprocess.run(["python", "karakter.py"])  # karakter.py dosyasını çalıştır

def run_item_giydir():
    """Item giydirme işlemini başlat"""
    print("Item giydirme işlemi başlatılıyor...")
    subprocess.run(["python", "itemgiy.py"])  # itemgiy.py dosyasını çalıştır

def main():
    clear_screen()
    print_header()

    while True:
        print_menu()
        choice = input().strip()

        if choice == "1":
            run_bot()  # Botu başlat

        elif choice == "2":
            clear_screen()
            print_header()
            # Brear token güncelleme işlemleri
            pass  # Buraya güncelleme kodunu ekleyin

        elif choice == "3":
            run_character_creation()  # Karakter oluşturma işlemini başlat

        elif choice == "4":
            run_item_giydir()  # Item giydirme işlemini başlat

        elif choice == "5":
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
