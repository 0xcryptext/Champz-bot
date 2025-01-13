# Champz Bot

Champz Bot, Champz oyununda otomatik karakter oluşturma ve item giydirme işlemlerini gerçekleştiren bir Python botudur. Bu bot, kullanıcıların oyun içindeki işlemlerini kolaylaştırmak için tasarlanmıştır.

## Özellikler

- **Botu Başlatma:** Oyun botunu başlatmak için kullanılır.
- **BREAR Güncelleme:** Kullanıcı brear bilgilerinizi güncelleyebilirsiniz (HERGÜN GÜNCELLEME GEREKLİ BAZEN GÜN İÇERİSİNDE DE GEREKLİ OLABİLİYOR).
- **Karakter Oluşturma:** Oyun içinde yeni karakterler oluşturabilirsiniz.
- **Item Giydirme:** Karakterlerinize otomatik olarak item giydirebilirsiniz.

## Gereksinimler

- Python 3.8 veya daha yeni bir sürüm
- Gerekli Python kütüphaneleri (otomatik olarak yüklenir)

## Kurulum

1. **Depoyu Klonlayın:**
   ```bash
   git clone https://github.com/kullaniciadi/champz-bot.git
   cd champz-bot
   ```

2. **Gerekli Kütüphaneleri Yükleyin:**
   - Sanal ortam otomatik olarak `run.bat` dosyası tarafından oluşturulacak ve gerekli kütüphaneler yüklenecektir. Kullanıcı sadece aşağıdaki komutu çalıştırmalıdır:
   ```bash
   run.bat
   ```

3. **Wallet.json Dosyasını Oluşturun:**
   - `data` klasöründe `wallet.json` dosyasını oluşturun ve cüzdan bilgilerinizi aşağıdaki gibi ekleyin.
   ```json
   [
       {
           "address": "Cüzdan adresinizi buraya ekleyin",
           "private_key": "Özel anahtarınızı buraya ekleyin"
       },
       {
           "address": "Cüzdan adresinizi buraya ekleyin",
           "private_key": "Özel anahtarınızı buraya ekleyin"
       }
       // Daha fazla cüzdan eklemek için yukarıdaki yapıyı takip edin
   ]
   ```

## Kullanım

1. **Botu Başlatın:**
   ```bash
   run.bat
   ```

2. **Menü Seçeneklerini Takip Edin:**
   - 1: Botu Başlat
   - 2: Wallet Güncelle
   - 3: Karakterleri Oluştur
   - 4: Item Giydir
   - 5: Çıkış

## Katkıda Bulunma

Bu projeye katkıda bulunmak isterseniz, lütfen bir pull request gönderin veya sorunlarınızı bildirin.

## Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Daha fazla bilgi için [LICENSE](LICENSE) dosyasını kontrol edin.