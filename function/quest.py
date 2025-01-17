import json
import requests
import os
import time

# Define file paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
AUTH_FILE = os.path.join(DATA_DIR, "auth.json")

def load_tokens():
    try:
        with open(AUTH_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("auth.json file not found")
        return []

def get_quests(token):
    url = "https://api.champz.world/quests/current"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {token}",
        "origin": "https://play.champz.world"
    }
    
    try:
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Request error: {e}")
        return None

def accept_quest(token, quest_id):
    url = "https://api.champz.world/quests/accept"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {token}",
        "origin": "https://play.champz.world"
    }
    data = {"quest_id": quest_id}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Quest acceptance error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Request error: {e}")
        return None

def redraw_quest(token, quest_id):
    url = "https://api.champz.world/quests/redraw"
    headers = {
        "accept": "application/json",
        "content-type": "application/json", 
        "authorization": f"Bearer {token}",
        "origin": "https://play.champz.world"
    }
    data = {"quest_id": quest_id}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Quest redraw error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Request error: {e}")
        return None

def dismiss_quest(token, quest_id):
    url = "https://api.champz.world/quests/dismiss"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {token}",
        "origin": "https://play.champz.world"
    }
    data = {"quest_id": quest_id}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Quest dismiss error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Request error: {e}")
        return None

def display_quests(quests):
    print("\nAKTİF GÖREVLER:")
    print("-" * 20)
    
    # Group quests by type - note the capital F in "Fight"
    daily_quests = [q for q in quests if q.get("quest_type") == "Daily"]
    fight_quests = [q for q in quests if q.get("quest_type") == "Fight"]
    other_quests = [q for q in quests if q.get("quest_type") not in ["Daily", "Fight"]]
    
    # Display Daily quests
    for quest in daily_quests:
        print(f"► Görev ID: {quest.get('id')}")
        print(f"  Görev Tipi: Daily")
        print("-" * 20)
    
    # Display Fight quests
    for quest in fight_quests:
        print(f"► Görev ID: {quest.get('id')}")
        print(f"  Görev Tipi: Fight")
        print("-" * 20)
    
    # Display Other quests
    for quest in other_quests:
        print(f"► Görev ID: {quest.get('id')}")
        print(f"  Görev Tipi: {quest.get('quest_type')}")
        print("-" * 20)

def check_quests():
    tokens = load_tokens()
    
    for account_index, token in enumerate(tokens, 1):
        print("\n" + "="*50)
        print(f"HESAP {account_index}")
        print("="*50)
        
        quest_data = get_quests(token)
        if quest_data and quest_data.get("success"):
            quests = quest_data.get("quests", [])
            if not quests:
                print("Bu hesapta aktif görev bulunamadı")
                continue
            
            display_quests(quests)
            
            # Accept non-daily quests
            print("\nGÖREVLER KABUL EDİLİYOR:")
            print("-" * 20)
            for quest in quests:
                quest_id = quest.get("id")
                quest_type = quest.get("quest_type")
                if quest_type != "daily":
                    print(f"► Görev {quest_id} ({quest_type}) kabul ediliyor...")
                    result = accept_quest(token, quest_id)
                    if result and result.get("success"):
                        print(f"  ✓ Görev başarıyla kabul edildi")
                    else:
                        print(f"  ✗ Görev kabul edilemedi")
                    time.sleep(2)
            
            # Get updated quest list
            updated_quests = get_quests(token).get("quests", [])
            
            # Dismiss non-fight and non-daily quests
            print("\nFIGHT VE DAILY DIŞI GÖREVLER İPTAL EDİLİYOR:")
            print("-" * 20)
            for quest in updated_quests:
                quest_id = quest.get("id")
                quest_type = quest.get("quest_type")
                if quest_type not in ["Fight", "Daily"]:  # Skip both Fight and Daily
                    print(f"► Görev {quest_id} ({quest_type}) iptal ediliyor...")
                    result = dismiss_quest(token, quest_id)
                    if result and result.get("success"):
                        print(f"  ✓ Görev başarıyla iptal edildi")
                    else:
                        print(f"  ✗ Görev iptal edilemedi")
                    time.sleep(2)

if __name__ == "__main__":
    check_quests()