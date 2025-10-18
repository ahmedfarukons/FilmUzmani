"""
IMDb Dataset İndirme Script'i
Kaggle'dan IMDb film yorumları dataset'ini indirir
"""
import os
import sys
import zipfile
import json

def download_with_kaggle_api():
    """Kaggle API kullanarak dataset indir"""
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
        
        print("📥 Kaggle API ile IMDb dataset'i indiriliyor...")
        
        # Kaggle API'yi başlat
        api = KaggleApi()
        api.authenticate()
        
        # Dataset'i indir
        dataset_name = "lakshmi25npathi/imdb-dataset-of-50k-movie-reviews"
        download_path = "data/raw"
        
        # Klasörü oluştur
        os.makedirs(download_path, exist_ok=True)
        
        # Dataset'i indir
        api.dataset_download_files(
            dataset_name,
            path=download_path,
            unzip=True
        )
        
        print("✅ Dataset başarıyla indirildi!")
        print(f"📁 Konum: {download_path}")
        
        # İndirilen dosyaları listele
        files = os.listdir(download_path)
        print(f"\n📄 İndirilen dosyalar:")
        for file in files:
            print(f"  - {file}")
        
        return True
        
    except ImportError:
        print("❌ Kaggle paketi yüklü değil!")
        print("Lütfen şu komutu çalıştırın: pip install kaggle")
        return False
    
    except Exception as e:
        print(f"❌ Hata: {str(e)}")
        print("\n💡 Kaggle API kurulumu için:")
        print("1. https://www.kaggle.com/account adresinden API token indirin")
        print("2. kaggle.json dosyasını ~/.kaggle/ klasörüne koyun (Windows: C:\\Users\\YourUsername\\.kaggle\\)")
        print("3. pip install kaggle")
        return False


def check_kaggle_credentials():
    """Kaggle kimlik bilgilerini kontrol et"""
    kaggle_path = os.path.expanduser("~/.kaggle/kaggle.json")
    
    if os.path.exists(kaggle_path):
        print("✅ Kaggle kimlik bilgileri bulundu")
        return True
    else:
        print("⚠️ Kaggle kimlik bilgileri bulunamadı!")
        print("\n📝 Kurulum adımları:")
        print("1. https://www.kaggle.com/account sayfasına gidin")
        print("2. 'Create New API Token' butonuna tıklayın")
        print("3. İndirilen kaggle.json dosyasını şu konuma koyun:")
        print(f"   {kaggle_path}")
        return False


def main():
    """Ana fonksiyon"""
    print("=" * 60)
    print("🎬 IMDb Dataset İndirme Aracı")
    print("=" * 60)
    print()
    
    # Kimlik bilgilerini kontrol et
    if not check_kaggle_credentials():
        print("\n❌ Lütfen önce Kaggle API'yi yapılandırın.")
        return
    
    # Dataset'i indir
    success = download_with_kaggle_api()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ İndirme tamamlandı!")
        print("=" * 60)
        print("\n💡 Sonraki adım:")
        print("   python scripts/process_imdb_dataset.py")
    else:
        print("\n❌ İndirme başarısız oldu.")


if __name__ == "__main__":
    main()


