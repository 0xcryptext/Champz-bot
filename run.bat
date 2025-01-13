@echo off
echo Champz Bot Başlatılıyor...

:: Python'un yüklü olup olmadığını kontrol et
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python bulunamadi! Lutfen Python 3.8 veya daha yeni bir surum yukleyin.
    pause
    exit /b 1
)

:: Sanal ortamın var olup olmadığını kontrol et
if not exist "venv" (
    echo Sanal ortam olusturuluyor...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo Sanal ortam olusturulamadi!
        pause
        exit /b 1
    )
    
    :: Sanal ortamı aktifleştir
    call venv\Scripts\activate

    :: Gereksinimleri kontrol et ve yükle
    pip install -r requirements.txt
)

:: Sanal ortamı aktifleştir
call venv\Scripts\activate

:: run.py dosyasını başlat
python run.py
