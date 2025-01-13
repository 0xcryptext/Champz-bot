import json
import time
import random
from web3 import Web3
from eth_account.messages import encode_defunct
import requests
import os

# Dosya yolları için sabit değişkenler
DATA_DIR = "data"  # data klasörü
AUTH_FILE = os.path.join(DATA_DIR, "auth.json")
CHARACTERS_FILE = os.path.join(DATA_DIR, "characters.json")
FIGHT_ID_FILE = os.path.join(DATA_DIR, "fight_id.json")

def ensure_data_dir():
    """Data klasörünün varlığını kontrol et, yoksa oluştur"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_wallets():
    with open('wallet.json', 'r') as file:
        return json.load(file)

def load_auth():
    ensure_data_dir()
    try:
        with open(AUTH_FILE, 'r') as file:
            tokens = json.load(file)
            return tokens  # Direkt liste döndürülür
    except FileNotFoundError:
        # Dosya yoksa boş liste oluştur ve kaydet
        empty_list = []
        save_auth(empty_list)
        return empty_list
    except json.JSONDecodeError:
        # Dosya bozuksa veya boşsa yeni liste oluştur
        empty_list = []
        save_auth(empty_list)
        return empty_list

def save_auth(auth_data):
    ensure_data_dir()
    with open(AUTH_FILE, 'w') as file:
        json.dump(auth_data, file, indent=2)

def process_wallet(private_key, address):
    w3 = Web3(Web3.HTTPProvider('https://rpc.ankr.com/eth'))
    
    message = f"Welcome Champ! Click to sign in and accept our Terms of Service and Privacy Policy (https://champz.world/terms). Verify your address {address} v2.0"
    
    message_to_sign = encode_defunct(text=message)
    signed_message = w3.eth.account.sign_message(message_to_sign, private_key)
    signature = "0x" + signed_message.signature.hex()
    
    url = "https://api.champz.world/game/register"
    headers = {
        "accept": "application/json",
        "accept-language": "tr-TR,tr;q=0.9",
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
    
    data = {
        "address": address,
        "signature": signature
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.ok:
        return response.json().get('jwt')
    return None

def main():
    # Başlangıçta auth.json dosyasını sil
    if os.path.exists(AUTH_FILE):
        os.remove(AUTH_FILE)
        print("Eski auth.json dosyası silindi. Yeni tokenlar alınacak.")
    
    wallets = load_wallets()
    auth_tokens = []  # Boş liste ile başla
    
    print(f"Toplam {len(wallets)} cüzdan işlenecek...")
    
    for wallet in wallets:
        address = wallet['address']
        private_key = wallet['private_key']
        
        print(f"\nİşleniyor: {address}")
        
        jwt_token = process_wallet(private_key, address)
        
        if jwt_token:
            auth_tokens.append(jwt_token)  # Token'ı listeye ekle
            save_auth(auth_tokens)  # Her başarılı işlemde kaydet
            print(f"✅ Başarılı: {address}")
            print(f"Bearer Token: {jwt_token[:30]}...")
            print(f"Toplam alınan token sayısı: {len(auth_tokens)}")
        else:
            print(f"❌ Hata: {address}")
        
        sleep_time = random.uniform(5, 12)
        print(f"Bekleniyor: {sleep_time:.2f} saniye...")
        time.sleep(sleep_time)
    
    print("\nİşlem tamamlandı!")
    print(f"Toplam {len(auth_tokens)} token alındı ve kaydedildi.")

if __name__ == "__main__":
    main()
