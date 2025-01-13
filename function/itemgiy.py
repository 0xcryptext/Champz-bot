import json
import requests
import os

# Dosya yolları
DATA_DIR = "data"
AUTH_FILE = os.path.join(DATA_DIR, "auth.json")

def load_tokens():
    """Auth dosyasından token'ları yükle"""
    try:
        with open(AUTH_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("auth.json dosyası bulunamadı!")
        return []

def get_characters(token):
    """Karakterleri listele"""
    url = "https://api.champz.world/game/charlist"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {token}"
    }
    
    response = requests.post(url, headers=headers)
    if response.ok:
        return response.json().get("charlist", [])
    return []

def get_items(token):
    """Hesaptaki itemları listele"""
    url = "https://api.champz.world/player/itemlist"
    headers = {
        "accept": "application/json",
        "accept-language": "tr-TR,tr;q=0.9",
        "authorization": f"Bearer {token}",
        "origin": "https://play.champz.world",
        "referer": "https://play.champz.world/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    
    response = requests.post(url, headers=headers)
    if response.ok:
        return response.json()
    return None

def equip_item(token, char_id, item_id, slot_id):
    """İtemi karaktere giydir"""
    url = "https://api.champz.world/char/equip"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {token}",
        "content-type": "application/json",
        "origin": "https://play.champz.world"
    }
    
    data = {
        "char": char_id,
        "slot_id": slot_id,
        "item_id": item_id
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.ok

def get_character_class(character):
    """Karakter sınıfını belirle"""
    class_id = character.get('class_id', 0)
    if class_id == 1:
        return "melee"
    elif class_id == 2:
        return "ranged"
    elif class_id == 3:
        return "magic"
    return "unknown"

def get_item_type(item):
    """Item tipini belirle"""
    weapon_class = item.get('weapon_class_id', 0)
    name = item.get('name', '').lower()
    
    if 'bow' in name or weapon_class == 2:
        return "ranged"
    elif 'axe' in name or weapon_class == 1:  # Axe kontrolü
        return "melee"
    elif 'staff' in name or weapon_class == 3:  # Staff kontrolü
        return "magic"
    elif 'shield' in name:  # Shield kontrolü
        return "shield"
    return "unknown"

def auto_equip_items(token, characters, items_data):
    """İtemleri otomatik olarak uygun karakterlere giydir"""
    if not items_data or not items_data.get("success"):
        print("İtemler alınamadı!")
        return

    items = items_data.get("itemlist", [])
    if not items:
        print("Hesapta item bulunamadı!")
        return

    # İtemleri ve karakterleri sınıflarına göre grupla
    melee_items = []
    ranged_items = []
    magic_items = []  # Magic itemleri için liste
    shield_items = []  # Shield itemleri için liste
    melee_chars = []
    ranged_chars = []
    magic_chars = []  # Magic karakterler için liste

    # İtemleri sınıflandır
    for item in items:
        item_type = get_item_type(item)
        min_level = item.get('min_lvl_equip', 1)
        
        if item_type == "melee":
            melee_items.append(item)
        elif item_type == "ranged":
            ranged_items.append(item)
        elif item_type == "magic":  # Magic itemlerini ayır
            magic_items.append(item)
        elif item_type == "shield":  # Shield itemlerini ayır
            shield_items.append(item)

    # Karakterleri sınıflandır
    for char in characters:
        char_type = get_character_class(char)
        if char_type == "melee":
            melee_chars.append(char)
        elif char_type == "ranged":
            ranged_chars.append(char)
        elif char_type == "magic":
            magic_chars.append(char)  # Magic karakterleri ekle

    equipped_count = 0
    equipped_items = set()  # Giydirilen item ID'lerini saklamak için

    # Melee karakterlere Axe giydir
    for char in melee_chars:
        suitable_items = [
            item for item in melee_items 
            if char.get('lvl', 0) >= item.get('min_lvl_equip', 1) and item['item_id'] not in equipped_items
        ]
        if suitable_items:
            best_item = max(suitable_items, key=lambda x: x.get('item_lvl', 0))
            if equip_item(token, char['id'], best_item['item_id'], best_item['slot_id']):
                print(f"✅ {char.get('name')} karakterine {best_item.get('name')} giydirildi!")
                equipped_count += 1
                equipped_items.add(best_item['item_id'])  # Giydirilen itemi ekle

    # Ranged karakterlere Bow giydir
    for char in ranged_chars:
        suitable_items = [
            item for item in ranged_items 
            if char.get('lvl', 0) >= item.get('min_lvl_equip', 1) and item['item_id'] not in equipped_items
        ]
        if suitable_items:
            best_item = max(suitable_items, key=lambda x: x.get('item_lvl', 0))
            if equip_item(token, char['id'], best_item['item_id'], best_item['slot_id']):
                print(f"✅ {char.get('name')} karakterine {best_item.get('name')} giydirildi!")
                equipped_count += 1
                equipped_items.add(best_item['item_id'])  # Giydirilen itemi ekle

    # Magic karakterlere Staff giydir
    for char in magic_chars:
        suitable_items = [
            item for item in magic_items 
            if char.get('lvl', 0) >= item.get('min_lvl_equip', 1) and item['item_id'] not in equipped_items
        ]
        if suitable_items:
            best_item = max(suitable_items, key=lambda x: x.get('item_lvl', 0))
            if equip_item(token, char['id'], best_item['item_id'], best_item['slot_id']):
                print(f"✅ {char.get('name')} karakterine {best_item.get('name')} giydirildi!")
                equipped_count += 1
                equipped_items.add(best_item['item_id'])  # Giydirilen itemi ekle

    # Tüm karakterlere Shield giydir
    for char in characters:
        suitable_shields = [
            item for item in shield_items 
            if char.get('lvl', 0) >= item.get('min_lvl_equip', 1) and item['item_id'] not in equipped_items
        ]
        if suitable_shields:
            best_shield = max(suitable_shields, key=lambda x: x.get('item_lvl', 0))
            if equip_item(token, char['id'], best_shield['item_id'], best_shield['slot_id']):
                print(f"✅ {char.get('name')} karakterine {best_shield.get('name')} giydirildi!")
                equipped_count += 1
                equipped_items.add(best_shield['item_id'])  # Giydirilen itemi ekle

    return equipped_count

def main():
    tokens = load_tokens()
    if not tokens:
        print("Token bulunamadı!")
        return
    
    print(f"Toplam {len(tokens)} hesap kontrol edilecek...\n")
    
    for i, token in enumerate(tokens, 1):
        print(f"\n{'='*50}")
        print(f"Hesap {i}/{len(tokens)} kontrol ediliyor...")
        print(f"{'='*50}\n")
        
        characters = get_characters(token)
        if not characters:
            print("❌ Karakterler alınamadı!")
            continue
            
        print(f"Toplam {len(characters)} karakter bulundu.")
        
        items_data = get_items(token)
        if items_data:
            equipped = auto_equip_items(token, characters, items_data)
            print(f"\nToplam {equipped} item başarıyla giydirildi!")
        else:
            print("❌ İtemler alınamadı!")
        
        input("\nDevam etmek için Enter'a basın...")

if __name__ == "__main__":
    main()
