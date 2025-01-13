import json
import requests
import time
import random
import os

# Dosya yolları
DATA_DIR = "data"
AUTH_FILE = os.path.join(DATA_DIR, "auth.json")
CHARACTERS_FILE = os.path.join(DATA_DIR, "characters.json")

def load_tokens():
    """Auth dosyasından token'ları yükle"""
    try:
        with open(AUTH_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("auth.json dosyası bulunamadı!")
        return []

def get_character_count(token):
    """Mevcut karakter sayısını kontrol et"""
    url = "https://api.champz.world/game/charlist"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {token}"
    }
    
    response = requests.post(url, headers=headers)
    if response.ok:
        data = response.json()
        return len(data.get("charlist", []))
    return 0

def create_character(token):
    """Yeni karakter oluştur"""
    url = "https://api.champz.world/char/create/f2p"
    headers = {
        "accept": "application/json",
        "accept-language": "tr-TR,tr;q=0.9",
        "authorization": f"Bearer {token}",
        "content-type": "application/json",
        "origin": "https://play.champz.world",
        "priority": "u=1, i",
        "referer": "https://play.champz.world/",
        "sec-ch-ua": '"Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    
    data = {"class_id": 0}  # Varsayılan sınıf
    
    response = requests.post(url, headers=headers, json=data)
    return response.ok

def main():
    tokens = load_tokens()
    if not tokens:
        print("Token bulunamadı!")
        return
    
    print(f"Toplam {len(tokens)} hesap işlenecek...")
    
    for i, token in enumerate(tokens, 1):
        print(f"\nHesap {i}/{len(tokens)} işleniyor...")
        
        # Mevcut karakter sayısını kontrol et
        char_count = get_character_count(token)
        needed_chars = 6 - char_count
        
        print(f"Mevcut karakter sayısı: {char_count}")
        print(f"Oluşturulması gereken karakter sayısı: {needed_chars}")
        
        if needed_chars <= 0:
            print("Bu hesapta yeterli karakter var, geçiliyor...")
            continue
        
        # Gerekli sayıda karakter oluştur
        for j in range(needed_chars):
            print(f"\nKarakter {j+1}/{needed_chars} oluşturuluyor...")
            
            if create_character(token):
                print("✅ Karakter başarıyla oluşturuldu!")
            else:
                print("❌ Karakter oluşturulamadı!")
            
            # API limitlerini aşmamak için bekleme
            sleep_time = random.uniform(2, 5)
            print(f"Bekleniyor: {sleep_time:.2f} saniye...")
            time.sleep(sleep_time)
        
        # Hesaplar arası bekleme
        if i < len(tokens):
            sleep_time = random.uniform(5, 10)
            print(f"\nSonraki hesaba geçmeden önce bekleniyor: {sleep_time:.2f} saniye...")
            time.sleep(sleep_time)
    
    print("\nTüm işlemler tamamlandı!")

if __name__ == "__main__":
    main()
