import json
import requests
import time
import random
import os

# Dosya yolları için sabit değişkenler
DATA_DIR = "data"  # data klasörü
AUTH_FILE = os.path.join(DATA_DIR, "auth.json")
CHARACTERS_FILE = os.path.join(DATA_DIR, "characters.json")
FIGHT_ID_FILE = os.path.join(DATA_DIR, "fight_id.json")

# Auth dosyasındaki tokenları yükleme
def load_tokens_from_auth():
    try:
        with open(AUTH_FILE, 'r') as file:
            tokens = json.load(file)
            return tokens  # Direkt liste döndürülür
    except FileNotFoundError:
        return []  # Dosya yoksa boş liste döner

# Karakterleri güncelleyen işlev
def update_characters(token):
    url = "https://api.champz.world/game/charlist"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {token}",
    }
    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        charlist = data.get("charlist", [])
        characters = []

        for char_info in charlist:
            char_data = {
                "id": char_info.get("id"),
                "name": char_info.get("name"),
                "hp": char_info.get("hp"),
                "ap": char_info.get("ap"),
                "exp": char_info.get("exp"),
                "lvl": char_info.get("lvl"),
                "max_exp": char_info.get("max_exp"),
                "hp_base": char_info.get("hp_base"),
            }
            characters.append(char_data)

        # Dosya yolunu güncelle
        with open(CHARACTERS_FILE, "w", encoding="utf-8") as file:
            json.dump(characters, file, indent=4, ensure_ascii=False)
        print("Karakter bilgileri güncellendi.")
    else:
        print(f"Karakter bilgileri alınamadı: {response.status_code}")

# Revive işlevi
def revive(token):
    with open(CHARACTERS_FILE, "r", encoding="utf-8") as file:
        characters = json.load(file)
        revived_characters = []

        for character in characters:
            if character.get("hp") == 0:
                character_id = character.get("id")
                character_name = character.get("name")
                url = "https://api.champz.world/char/revive"
                headers = {
                    "accept": "application/json",
                    "authorization": f"Bearer {token}",
                    "content-type": "application/json"
                }
                data = {
                    "char": character_id
                }
                response = requests.post(url, headers=headers, json=data)

                if response.status_code == 200:
                    revived_characters.append(character_name)
                    print(f"Karakter {character_name} (ID: {character_id}) revive edildi.")
                else:
                    print(f"Revive API isteği başarısız oldu: {response.status_code}")
        
        if revived_characters:
            print(f"Revive edilen karakterler: {', '.join(revived_characters)}")
        else:
            print("HP değeri 0 olan karakter bulunamadı.")
        
        wait_time = random.randint(3, 6)
        print(f"Revive işleminden sonra {wait_time} saniye bekleniyor...")
        time.sleep(wait_time)

# Heal işlevi (HP'si hp_base'den küçük olan karakterler iyileştirilecek)
def heal(token):
    with open(CHARACTERS_FILE, "r", encoding="utf-8") as file:
        characters = json.load(file)
    
    for character in characters:
        # Get 'hp' and 'hp_base' values safely with default values of 0 if None
        hp = character.get("hp", 0)
        hp_base = character.get("hp_base", 0)
        
        # Check if hp is less than hp_base before proceeding
        if hp is not None and hp_base is not None and hp < hp_base:
            character_id = character.get("id")
            url = "https://api.champz.world/char/heal"
            headers = {
                "accept": "application/json",
                "authorization": f"Bearer {token}",
                "content-type": "application/json"
            }
            data = {
                "char": character_id
            }
            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                print(f"Karakter {character['name']} (ID: {character_id}) heal edildi.")
            else:
                print(f"Heal API isteği başarısız oldu: {response.status_code}")


# Savaş işlevi
def fight(token):
    with open(CHARACTERS_FILE, "r", encoding="utf-8") as file:
        characters_data = json.load(file)

    selected_character = None
    for char in characters_data:
        ap = char.get('ap', 0)
        hp = char.get('hp', 0)
        if ap > 0 and hp > 0:
            selected_character = char
            break

    if selected_character:
        char_id = selected_character['id']
        char_name = selected_character['name']
        url = "https://api.champz.world/fight"
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {token}",
            "content-type": "application/json"
        }
        data = {
            "charlist": [char_id],
            "origin": "/char"
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            fight_data = response.json()
            fight_id = fight_data.get("fight", {}).get("id")

            if fight_id:
                print(f"Savaş başlatıldı. Fight ID: {fight_id}")
                with open(FIGHT_ID_FILE, "w", encoding="utf-8") as file:
                    json.dump({"fight_id": fight_id}, file, indent=4)
            else:
                print("Fight ID alınamadı.")
        else:
            print(f"Fight API isteği başarısız oldu: {response.status_code}")

        wait_time = random.randint(3, 8)
        print(f"Savaş işleminden sonra {wait_time} saniye bekleniyor...")
        time.sleep(wait_time)
    else:
        print("AP ve HP değeri 0'dan büyük bir karakter bulunamadı.")

# Fight Skip işlevi
def fight_skip(token):
    try:
        # Dosya yolunu güncelle
        with open(FIGHT_ID_FILE, "r", encoding="utf-8") as file:
            fight_data = json.load(file)
    except FileNotFoundError:
        print("fight_id.json dosyası bulunamadı.")
        return
    except json.JSONDecodeError:
        print("fight_id.json dosyasının içeriği geçersiz.")
        return

    fight_id = fight_data.get("fight_id")

    if fight_id:
        url = "https://api.champz.world/fight/skipToTheEnd"
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {token}",
            "content-type": "application/json"
        }
        data = {
            "fight_id": str(fight_id)
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            print(f"Fight Skip başarılı. Fight ID: {fight_id}")
        else:
            print(f"Fight Skip API isteği başarısız oldu: {response.status_code} - {response.text}")
    else:
        print("Geçerli bir fight_id bulunamadı.")

# Daily Claim işlevi
def get_active_days(token):
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
                        active_days = quest.get("last_claim_day", 0)
                        print(f"Active Days: {active_days}")
                        return active_days
            print("Aktif gün verisi bulunamadı.")
        else:
            print(f"API isteği başarısız oldu. Hata kodu: {response.status_code}")
            print("Hata mesajı:", response.text)

    except requests.RequestException as e:
        print(f"API isteği sırasında bir hata oluştu: {e}")

    return None

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


def should_claim_daily_login(quest_data, active_days):
    """
    Daily Login görevi claim edilmeli mi?
    Eğer last_claim_day, active_days'e eşit değilse claim edilmesi gerekiyor.
    """
    last_claim_day = quest_data.get("last_claim_day", 0)

    if last_claim_day != active_days:
        return True  # Claim yapılmalı
    return False  # Claim yapılmamalı

def claim_quest(quest_id, token):
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
            print("Quest başarıyla claim edildi!")
            print("Cevap:", response.json())
        else:
            print(f"Claim API isteği başarısız oldu. Hata kodu: {response.status_code}")
            print("Hata mesajı:", response.text)

    except requests.RequestException as e:
        print(f"Claim API isteği sırasında bir hata oluştu: {e}")


def main():
    BEARER_TOKENS = load_tokens_from_auth()  # Auth dosyasından tokenları yükle
    
    if not BEARER_TOKENS:
        print("auth.json dosyasından token alınamadı veya boş.")
        return

    for token in BEARER_TOKENS:
        print(f"Token {token} ile işlemler başlatılıyor...")

        # İlk olarak Daily Quest claim işlemi yapılacak
        print("Daily Quest claim ediliyor...")
        active_days = get_active_days(token)
        
        if active_days is not None:
            print(f"Aktif gün sayısı: {active_days}")
                
            # Daily Login görevi alınır ve claim edilir
            quest_data = get_daily_login_quest_id(token)
            if quest_data:
                if should_claim_daily_login(quest_data, active_days):
                    print("Daily Login görevi claim edilecek...")
                    claim_quest(quest_data['id'], token)
                else:
                    print("Daily Login görevi zaten claim edilmiş, işlem yapılmadı.")
        else:
            print("Aktif gün bilgisi alınamadı, günlük ödül alınamayacak.")

        # Günlük ödül claim işlemi yalnızca bir kez yapılacak
        print("Günlük ödül alınıyor...")
        if quest_data:
            claim_quest(quest_data['id'], token)  # Yalnızca bir kez günlük ödül claim edilir

        # Karakterlerin AP değeri 0 olana kadar işlemler devam edecek
        while True:
            print("Karakter bilgileri güncelleniyor...")
            update_characters(token)  # Karakter bilgileri güncellenir

            with open(CHARACTERS_FILE, "r", encoding="utf-8") as file:
                characters_data = json.load(file)

            # HP'si 0 olan karakterleri filtrele ve revive et
            characters_to_revive = [char for char in characters_data if char.get("hp", 0) == 0]

            if characters_to_revive:
                print("HP değeri 0 olan karakterler revive ediliyor...")
                revive(token)  # Revive işlemi yapılır

            # Heal işlemi: Canı eksik olan karakterlere heal yapılır
            print("Canı eksik olan karakterlere heal işlemi yapılıyor...")
            heal(token)

            # AP'si 0'dan büyük olan karakterleri filtrele
            characters_with_ap = [char for char in characters_data if char.get('ap', 0) > 0]

            if characters_with_ap:
                # Savaş başlatılır
                print("Savaş başlatılıyor...")
                fight(token)
                
                print("Savaş atlanıyor...")
                fight_skip(token)

            else:
                # Eğer tüm karakterlerin AP değeri 0 ise işlemler durur
                print(f"{token} için AP değeri 0 olan tüm karakterler var. Bir sonraki tokena geçiliyor.")
                break

            # Bekleme süresi (isteğe bağlı)
            time.sleep(2)  # İki saniye beklemek, işlemi hızlandırmamak için

if __name__ == "__main__":
    main()
