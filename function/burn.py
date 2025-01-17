import os
import json
import random
import requests
import time

# Define file paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
AUTH_FILE = os.path.join(DATA_DIR, "auth.json")

def load_tokens():
    try:
        with open(AUTH_FILE, 'r') as f:
            tokens = json.load(f)  # JSON file contains direct array of tokens
            return tokens if isinstance(tokens, list) else []
    except FileNotFoundError:
        print(f"Error: {AUTH_FILE} not found")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {AUTH_FILE}")
        return []

def burn_spores(token):
    url = "https://api.champz.world/game/spores/burn"
    headers = {
        "sec-ch-ua-platform": "\"Android\"",
        "Authorization": f"Bearer {token}",
        "Referer": "https://play.champz.world/",
        "Accept-Language": "tr-TR,tr;q=0.9",
        "sec-ch-ua": "\"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    burn_amount = random.randint(1000, 1400)
    data = {"burn": burn_amount}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print(f"✓ {burn_amount} spores yakıldı")
            return response.json()
        else:
            print(f"✗ Hata: {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ İstek hatası: {e}")
        return None

def process_accounts():
    tokens = load_tokens()
    
    for account_index, token in enumerate(tokens, 1):
        print("\n" + "="*50)
        print(f"HESAP {account_index}")
        print("="*50)
        
        result = burn_spores(token)
        if result and result.get("success"):
            print("İşlem başarılı!")
        else:
            print("İşlem başarısız!")
        
        time.sleep(2)  # Rate limiting için bekleme

if __name__ == "__main__":
    process_accounts()