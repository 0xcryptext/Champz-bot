import requests
import json
import os
import time
import random

# Ana dizine göre dosya yolları için sabit değişkenler
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))  # function klasörü
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)  # ana dizin
DATA_DIR = os.path.join(PROJECT_ROOT, "data")  # data klasörü
AUTH_FILE = os.path.join(DATA_DIR, "auth.json")

# Auth dosyasındaki tokenları yükleme
def load_tokens():
    try:
        with open(AUTH_FILE, 'r') as file:
            tokens = json.load(file)
            return tokens  # Tüm tokenları döndür
    except (FileNotFoundError, json.JSONDecodeError):
        print("auth.json dosyasından token alınamadı veya dosya geçersiz.")
        return []

def get_treasures(token):
    """API'den tüm consumables'ı alır ve type'ı 'Treasure' olanları döner."""
    url = "https://api.champz.world/consumables/all"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {token}",
    }

    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            treasures = [item for item in data.get("consumables", []) if item.get("type") == "Treasure"]
            return treasures
        else:
            print("API isteği başarısız oldu.")
    else:
        print(f"API isteği başarısız oldu. Hata kodu: {response.status_code}")
        print("Hata mesajı:", response.text)

    return []

def open_chest(token, consumable_id):
    """Bir chest'i açmak için API çağrısı yapar."""
    url = "https://api.champz.world/consumables/open"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {token}",
        "content-type": "application/json",
    }
    data = {
        "consumable_id": consumable_id
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            print(f"Chest (ID: {consumable_id}) başarıyla açıldı!")
            return True  # Başarılı açma durumunda True döner
        else:
            print(f"Chest (ID: {consumable_id}) açılamadı! API cevabı: {data}")
    else:
        print(f"Chest (ID: {consumable_id}) açılamadı! Hata kodu: {response.status_code}")
        print("Hata mesajı:", response.text)

    return False  # Başarısız açma durumunda False döner

def main():
    # Token'ları yükle
    tokens = load_tokens()
    if not tokens:
        return  # Token alınamazsa işlemi sonlandır

    for index, token in enumerate(tokens, start=1):
        print(f"{index}. hesap ile chest açma işlemi başlatılıyor...")

        # Treasure itemlerini al
        treasures = get_treasures(token)
        if treasures:
            print("Treasure itemleri:")
            for treasure in treasures:
                print(f"- İsim: {treasure['name']}, ID: {treasure['id']}, Adet: {treasure['balance']}")

                # Chest'i açmaya devam et
                while treasure['balance'] > 0:
                    if open_chest(token, treasure['id']):
                        treasure['balance'] -= 1  # Miktarı bir azalt
                    else:
                        break  # Açma işlemi başarısız olursa döngüden çık

                    # 2-4 saniye bekle
                    wait_time = random.randint(2, 4)
                    print(f"Bir sonraki chest açılmadan önce {wait_time} saniye bekleniyor...")
                    time.sleep(wait_time)

                print(f"Chest (ID: {treasure['id']}) için açma işlemleri tamamlandı. Kalan miktar: {treasure['balance']}")
        else:
            print("Treasure itemi bulunamadı.")

        # Her hesap arasında 5-12 saniye bekle
        if index < len(tokens):  # Son hesap değilse bekle
            wait_time = random.randint(5, 12)
            print(f"\nBir sonraki hesaba geçmeden önce {wait_time} saniye bekleniyor...")
            time.sleep(wait_time)

if __name__ == "__main__":
    main()
