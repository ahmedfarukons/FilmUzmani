"""
IMDb Dataset İşleme Script'i
CSV formatındaki IMDb yorumlarını metin dosyalarına dönüştürür
"""
import os
import pandas as pd
from pathlib import Path


def process_imdb_csv():
    """IMDb CSV dosyasını işle ve metin dosyalarına dönüştür"""
    try:
        # CSV dosyasını bul
        csv_path = "data/raw/IMDB Dataset.csv"
        
        if not os.path.exists(csv_path):
            print(f"❌ CSV dosyası bulunamadı: {csv_path}")
            print("💡 Önce download_imdb_dataset.py script'ini çalıştırın")
            return False
        
        print("📊 IMDb dataset'i işleniyor...")
        
        # CSV'yi oku
        df = pd.read_csv(csv_path)
        print(f"✓ {len(df)} yorum yüklendi")
        
        # Veri yapısını kontrol et
        print(f"✓ Kolonlar: {df.columns.tolist()}")
        
        # Backup klasörünü oluştur
        backup_path = "data/backup"
        os.makedirs(backup_path, exist_ok=True)
        
        # Mevcut sample_reviews.txt'yi backup'la
        if os.path.exists("data/sample_reviews.txt"):
            print("📦 Mevcut veriler backup'lanıyor...")
            os.rename("data/sample_reviews.txt", "data/backup/sample_reviews_backup.txt")
            print("✓ Backup tamamlandı")
        
        # Her 5000 yorumu bir dosyaya yaz
        chunk_size = 5000
        num_chunks = (len(df) + chunk_size - 1) // chunk_size
        
        print(f"\n📝 {num_chunks} dosya oluşturuluyor...")
        
        for i in range(num_chunks):
            start_idx = i * chunk_size
            end_idx = min((i + 1) * chunk_size, len(df))
            chunk_df = df.iloc[start_idx:end_idx]
            
            # Dosya adı
            filename = f"data/imdb_reviews_{i+1:02d}.txt"
            
            # Dosyaya yaz
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"IMDb Film Yorumları - Bölüm {i+1}\n")
                f.write(f"{'=' * 80}\n\n")
                
                for idx, row in chunk_df.iterrows():
                    review = row['review']
                    sentiment = row['sentiment']
                    
                    # Her yorumu formatla
                    f.write(f"Film Yorumu #{idx + 1}\n")
                    f.write(f"{'-' * 80}\n")
                    f.write(f"Değerlendirme: {sentiment}\n\n")
                    f.write(f"{review}\n\n")
                    f.write(f"{'=' * 80}\n\n")
            
            print(f"✓ Oluşturuldu: {filename} ({len(chunk_df)} yorum)")
        
        # İstatistikleri göster
        print("\n" + "=" * 80)
        print("📊 İstatistikler:")
        print(f"  Toplam yorum: {len(df)}")
        print(f"  Pozitif: {len(df[df['sentiment'] == 'positive'])}")
        print(f"  Negatif: {len(df[df['sentiment'] == 'negative'])}")
        print(f"  Oluşturulan dosya sayısı: {num_chunks}")
        print("=" * 80)
        
        print("\n✅ İşleme tamamlandı!")
        print("\n💡 Sonraki adım:")
        print("   Streamlit uygulamasını açın ve 'Verileri İşle' butonuna tıklayın")
        
        return True
        
    except Exception as e:
        print(f"❌ Hata: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def clean_old_files():
    """Eski IMDb dosyalarını temizle"""
    print("\n🗑️ Eski IMDb dosyalarını temizliyor...")
    
    data_dir = Path("data")
    imdb_files = list(data_dir.glob("imdb_reviews_*.txt"))
    
    if imdb_files:
        for file in imdb_files:
            file.unlink()
            print(f"✓ Silindi: {file.name}")
        print(f"✓ {len(imdb_files)} dosya temizlendi")
    else:
        print("✓ Temizlenecek dosya yok")


def main():
    """Ana fonksiyon"""
    print("=" * 80)
    print("🎬 IMDb Dataset İşleme Aracı")
    print("=" * 80)
    print()
    
    # İsteğe bağlı: Eski dosyaları temizle
    response = input("Mevcut IMDb dosyalarını temizlemek ister misiniz? (e/h): ").lower()
    if response == 'e':
        clean_old_files()
    
    print()
    
    # Dataset'i işle
    success = process_imdb_csv()
    
    if success:
        print("\n🎉 Hazır! Artık uygulamayı kullanabilirsiniz.")


if __name__ == "__main__":
    main()


