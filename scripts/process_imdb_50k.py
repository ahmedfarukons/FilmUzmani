"""
IMDb 50k Veri Seti İşleme Scripti
Kaggle'dan indirilen IMDb veri setini Film Gurusu formatına dönüştürür
"""
import os
import pandas as pd
import kagglehub
from pathlib import Path

def download_imdb_dataset():
    """IMDb 50k veri setini indirir"""
    print("📥 IMDb 50k veri seti indiriliyor...")
    
    try:
        # Kaggle'dan veri setini indir
        path = kagglehub.dataset_download("lakshmi25npathi/imdb-dataset-of-50k-movie-reviews")
        print(f"✅ Veri seti indirildi: {path}")
        return path
    except Exception as e:
        print(f"❌ İndirme hatası: {str(e)}")
        return None

def process_imdb_data(dataset_path):
    """IMDb veri setini işler ve Film Gurusu formatına dönüştürür"""
    print("🔄 Veri seti işleniyor...")
    
    try:
        # CSV dosyasını oku
        csv_file = os.path.join(dataset_path, "IMDB Dataset.csv")
        if not os.path.exists(csv_file):
            print(f"❌ CSV dosyası bulunamadı: {csv_file}")
            return False
        
        # Veriyi oku
        df = pd.read_csv(csv_file)
        print(f"📊 Toplam {len(df)} eleştiri yüklendi")
        
        # Pozitif ve negatif eleştirileri ayır
        positive_reviews = df[df['sentiment'] == 'positive']
        negative_reviews = df[df['sentiment'] == 'negative']
        
        print(f"✅ Pozitif eleştiriler: {len(positive_reviews)}")
        print(f"❌ Negatif eleştiriler: {len(negative_reviews)}")
        
        # Film Gurusu formatında dosya oluştur
        output_file = "data/imdb_50k_reviews.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("IMDb 50K FİLM ELEŞTİRİLERİ VERİ SETİ\n")
            f.write("=" * 50 + "\n\n")
            
            # Pozitif eleştirileri işle
            f.write("=== POZİTİF ELEŞTİRİLER ===\n\n")
            for idx, row in positive_reviews.head(1000).iterrows():  # İlk 1000 pozitif
                f.write(f"=== ELEŞTİRİ #{idx + 1} ===\n")
                f.write(f"Sentiment: Pozitif\n")
                f.write(f"Eleştiri:\n{row['review']}\n\n")
            
            # Negatif eleştirileri işle
            f.write("\n=== NEGATİF ELEŞTİRİLER ===\n\n")
            for idx, row in negative_reviews.head(1000).iterrows():  # İlk 1000 negatif
                f.write(f"=== ELEŞTİRİ #{idx + 1} ===\n")
                f.write(f"Sentiment: Negatif\n")
                f.write(f"Eleştiri:\n{row['review']}\n\n")
        
        print(f"✅ İşlenmiş veri kaydedildi: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ İşleme hatası: {str(e)}")
        return False

def main():
    """Ana fonksiyon"""
    print("🎬 IMDb 50k Veri Seti İşleme Başlıyor...")
    
    # Veri klasörünü oluştur
    os.makedirs("data", exist_ok=True)
    
    # Veri setini indir
    dataset_path = download_imdb_dataset()
    if not dataset_path:
        return
    
    # Veriyi işle
    if process_imdb_data(dataset_path):
        print("\n🎉 Başarıyla tamamlandı!")
        print("💡 Şimdi app.py'yi çalıştırıp 'Verileri İşle' butonuna tıklayabilirsiniz.")
    else:
        print("\n❌ İşlem başarısız!")

if __name__ == "__main__":
    main()
