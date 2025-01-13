import requests
import json
import os
import time
import random

# Dosya yolları için sabit değişkenler
DATA_DIR = "data"  # data klasörü
AUTH_FILE = os.path.join(DATA_DIR, "auth.json")
CHARACTERS_FILE = os.path.join(DATA_DIR, "characters.json")

# Auth dosyasındaki tokenları yükleme
def load_tokens():
    try:
        with open(AUTH_FILE, 'r') as file:
            tokens = json.load(file)
            return tokens  # Tüm tokenları döndür
    except (FileNotFoundError, json.JSONDecodeError):
        print("auth.json dosyasından token alınamadı veya dosya geçersiz.")
        return []

def get_daily_login_quest_id(token):
    url = "https://api.champz.world/quests/current"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {token}",
    }

    try:
        response = requests.post(url, headers=headers)

        if response.status_code == 200:
            data = response.json()

            if "quests" in data:
                for quest in data["quests"]:
                    if quest.get("description") == "Daily Login":
                        print(f"Daily Login Quest ID: {quest['id']}")
                        return quest
                print("'Daily Login' quest bulunamadı.")
            else:
                print("'quests' anahtarı JSON cevabında bulunamadı.")
        else:
            print(f"API isteği başarısız oldu. Hata kodu: {response.status_code}")
            print("Hata mesajı:", response.text)

    except requests.RequestException as e:
        print(f"API isteği sırasında bir hata oluştu: {e}")

    return None

def claim_daily_login_quest(quest_id, token):
    url = "https://api.champz.world/quests/claim"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {token}",
    }

    payload = {
        "quest_id": quest_id
    }

    try:
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("Quest başarıyla claim edildi!")
            else:
                print(f"Claim işlemi başarısız oldu. API yanıtı status: {data.get('status')}")
        else:
            print(f"Claim API isteği başarısız oldu. Hata kodu: {response.status_code}")
            print("Hata mesajı:", response.text)

    except requests.RequestException as e:
        print(f"Claim API isteği sırasında bir hata oluştu: {e}")

def main():
    # Token'ları yükle
    tokens = load_tokens()
    if not tokens:
        print("auth.json dosyasından token alınamadı veya boş.")
        return

    for index in range(len(tokens)):
        print(f"{index + 1}. hesap ile günlük quest claim ediliyor...")

        # Daily Login quest ID'sini al
        quest_data = get_daily_login_quest_id(tokens[index])
        if quest_data:
            claim_daily_login_quest(quest_data['id'], tokens[index])

        # İşlemler arasında 5-12 saniye bekle
        wait_time = random.randint(5, 12)
        print(f"{wait_time} saniye bekleniyor...")
        time.sleep(wait_time)

if __name__ == "__main__":
    main() 