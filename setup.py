# -*- coding: utf-8 -*-
"""
Film Gurusu Chatbot - Kurulum ve Veri İşleme Scripti
"""
import os
import sys
import io
from dotenv import load_dotenv
from src.data_processor import DataProcessor
from src.rag_pipeline import RAGPipeline

# Windows için UTF-8 encoding ayarla
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def check_api_key():
    """API key kontrolü yapar"""
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("❌ GEMINI_API_KEY / GOOGLE_API_KEY bulunamadı!")
        print("\n📝 Lütfen .env dosyası oluşturun ve API key'inizi ekleyin:")
        print("   GEMINI_API_KEY=your_api_key_here")
        print("   # veya")
        print("   GOOGLE_API_KEY=your_api_key_here")
        return None
    
    print("✅ API key bulundu")
    return api_key


def check_data_directory():
    """Veri dizinini kontrol eder"""
    if not os.path.exists('data'):
        print("❌ 'data' klasörü bulunamadı!")
        print("\n📝 Lütfen 'data' klasörü oluşturun ve film eleştirilerini içeren .txt dosyalarını ekleyin.")
        return False
    
    txt_files = [f for f in os.listdir('data') if f.endswith('.txt')]
    
    if len(txt_files) == 0:
        print("❌ 'data' klasöründe .txt dosyası bulunamadı!")
        return False
    
    print(f"✅ {len(txt_files)} adet veri dosyası bulundu")
    return True


def process_and_create_vectorstore(api_key: str):
    """Verileri işler ve vektör veritabanı oluşturur"""
    print("\n" + "="*60)
    print("🚀 VERİ İŞLEME VE VEKTÖR VERİTABANI OLUŞTURMA")
    print("="*60 + "\n")
    
    # 1. Veri işleme
    print("📊 ADIM 1: Veri İşleme (Chunking)")
    print("-" * 60)
    
    processor = DataProcessor(chunk_size=1000, chunk_overlap=200)
    documents = processor.process_directory('data')
    
    if len(documents) == 0:
        print("❌ İşlenecek veri bulunamadı!")
        return False
    
    print(f"\n✅ Toplam {len(documents)} chunk oluşturuldu\n")
    
    # 2. RAG Pipeline oluşturma
    print("🔧 ADIM 2: RAG Pipeline Başlatılıyor")
    print("-" * 60)
    
    rag = RAGPipeline(api_key=api_key)
    
    # 3. Vektör veritabanı oluşturma
    print("\n💾 ADIM 3: Vektör Veritabanı Oluşturuluyor")
    print("-" * 60)
    
    rag.create_vectorstore(documents)
    
    # 4. QA zinciri oluşturma
    print("\n🔗 ADIM 4: QA Zinciri Oluşturuluyor")
    print("-" * 60)
    
    rag.create_qa_chain(k=4)
    
    print("\n" + "="*60)
    print("✅ KURULUM BAŞARIYLA TAMAMLANDI!")
    print("="*60 + "\n")
    
    # Test sorgusu
    print("🧪 Test Sorgusu Çalıştırılıyor...")
    print("-" * 60)
    
    test_question = "Hangi filmler hakkında eleştiri var?"
    print(f"\nSoru: {test_question}\n")
    
    result = rag.query(test_question)
    print(f"Cevap:\n{result['answer']}\n")
    
    print("\n" + "="*60)
    print("🎉 HAZIR! Artık uygulamayı çalıştırabilirsiniz:")
    print("   streamlit run app.py")
    print("="*60 + "\n")
    
    return True


def main():
    """Ana kurulum fonksiyonu"""
    print("\n" + "="*60)
    print("🎬 FİLM GURUSU CHATBOT - KURULUM")
    print("="*60 + "\n")
    
    # 1. API key kontrolü
    print("1️⃣ API Key Kontrolü")
    print("-" * 60)
    api_key = check_api_key()
    if not api_key:
        sys.exit(1)
    
    print()
    
    # 2. Veri dizini kontrolü
    print("2️⃣ Veri Dizini Kontrolü")
    print("-" * 60)
    if not check_data_directory():
        sys.exit(1)
    
    print()
    
    # 3. Kullanıcıya onay sor
    print("3️⃣ Veri İşleme Onayı")
    print("-" * 60)
    print("Veriler işlenecek ve vektör veritabanı oluşturulacak.")
    print("Bu işlem birkaç dakika sürebilir.\n")
    
    response = input("Devam etmek istiyor musunuz? (E/H): ").strip().upper()
    
    if response != 'E':
        print("\n❌ Kurulum iptal edildi.")
        sys.exit(0)
    
    # 4. Veri işleme ve veritabanı oluşturma
    success = process_and_create_vectorstore(api_key)
    
    if not success:
        print("\n❌ Kurulum başarısız!")
        sys.exit(1)


if __name__ == "__main__":
    main()

