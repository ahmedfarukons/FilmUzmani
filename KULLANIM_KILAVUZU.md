# 🎬 Film Gurusu Chatbot - Kullanım Kılavuzu

Bu kılavuz, Film Gurusu chatbot'unu adım adım nasıl kurup kullanacağınızı gösterir.

## 📋 İçindekiler
1. [Hızlı Başlangıç](#hızlı-başlangıç)
2. [Detaylı Kurulum](#detaylı-kurulum)
3. [IMDb Dataset İndirme](#imdb-dataset-indirme)
4. [Web Arayüzü Kullanımı](#web-arayüzü-kullanımı)
5. [Sorun Giderme](#sorun-giderme)
6. [SSS](#sık-sorulan-sorular)

---

## 🚀 Hızlı Başlangıç

### 5 Dakikada Çalıştırın!

```bash
# 1. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 2. Ollama'yı başlatın
ollama serve

# 3. Phi-3 modelini indirin
ollama pull phi3:mini

# 4. Kaggle API yapılandırın (IMDb dataset için)
# kaggle.json dosyanızı ~/.kaggle/ klasörüne koyun

# 5. IMDb dataset'i indirin
python scripts/download_imdb_dataset.py

# 6. Dataset'i işleyin
python scripts/process_imdb_dataset.py

# 7. Uygulamayı başlatın
streamlit run app.py
```

Tarayıcınızda `http://localhost:8501` otomatik açılacak!

---

## 🔧 Detaylı Kurulum

### Adım 1: Python Kontrolü

```bash
python --version
```

✅ **Python 3.8 veya üzeri olmalı**

Eğer Python yüklü değilse:
- Windows: [python.org](https://www.python.org/downloads/)
- Mac: `brew install python3`
- Linux: `sudo apt install python3`

### Adım 2: Ollama Kurulumu

1. **Ollama'yı İndirin**
   - Windows/Mac/Linux: [https://ollama.com/download](https://ollama.com/download)

2. **Phi-3 Mini Modelini Çekin**
   ```bash
   ollama pull phi3:mini
   ```
   
   İndirme boyutu: ~2.3GB

3. **Ollama Servisini Başlatın**
   ```bash
   ollama serve
   ```
   
   Port: `http://localhost:11434`

4. **Kontrol Edin**
   ```bash
   ollama list
   # phi3:mini görünmeli
   ```

### Adım 3: Projeyi Hazırlayın

```bash
# Proje klasörüne gidin
cd FilmUzmani

# Virtual environment oluşturun (önerilen)
python -m venv venv

# Activate edin
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt
```

### Adım 4: Kaggle API Yapılandırması

IMDb dataset'i için Kaggle API gerekli:

1. **Kaggle Hesabı Oluşturun**
   - [https://www.kaggle.com](https://www.kaggle.com)

2. **API Token İndirin**
   - [https://www.kaggle.com/account](https://www.kaggle.com/account)
   - "Create New API Token" butonuna tıklayın
   - `kaggle.json` dosyası indirilecek

3. **Token'ı Yerleştirin**
   
   **Windows:**
   ```bash
   mkdir %USERPROFILE%\.kaggle
   copy kaggle.json %USERPROFILE%\.kaggle\
   ```
   
   **Mac/Linux:**
   ```bash
   mkdir -p ~/.kaggle
   cp kaggle.json ~/.kaggle/
   chmod 600 ~/.kaggle/kaggle.json
   ```

---

## 📊 IMDb Dataset İndirme

### Otomatik İndirme

```bash
# Dataset'i indir (50K IMDb yorumu)
python scripts/download_imdb_dataset.py
```

Script şunları yapacak:
- ✅ Kaggle kimlik bilgilerini kontrol eder
- ✅ IMDb Dataset'ini indirir (~66MB)
- ✅ Dosyaları `data/raw/` klasörüne çıkarır

### Dataset İşleme

```bash
# CSV'yi metin dosyalarına dönüştür
python scripts/process_imdb_dataset.py
```

Script şunları yapacak:
1. ✅ Mevcut sample_reviews.txt'yi backup'lar
2. ✅ CSV dosyasını okur (50,000 yorum)
3. ✅ Her 5000 yorumu bir dosyaya böler
4. ✅ `data/` klasörüne 10 dosya oluşturur

```
data/
├── imdb_reviews_01.txt  (5000 yorum)
├── imdb_reviews_02.txt  (5000 yorum)
├── ...
└── imdb_reviews_10.txt  (5000 yorum)
```

---

## 💻 Web Arayüzü Kullanımı

### Uygulamayı Başlatın

```bash
# Ollama servisinin çalıştığından emin olun
ollama serve

# Streamlit uygulamasını başlatın
streamlit run app.py
```

Tarayıcı otomatik açılacak. Açılmazsa: `http://localhost:8501`

### İlk Açılış

1. **Otomatik Başlatma**
   - Uygulama açıldığında sistem otomatik olarak RAG pipeline'ı yükler
   - `chroma_db/` varsa direkt kullanıma hazır!

2. **Veritabanı Yoksa**
   - Sol panelden "🔄 Verileri İşle / Güncelle" butonuna tıklayın
   - Sistem tüm `.txt` dosyalarını işleyecek
   - Vektör veritabanı oluşacak (~2-5 dakika)

### Arayüz Tanıtımı

#### Sol Panel (Sidebar)

**📊 Sistem Durumu**
- 🟢 **Sistem Hazır**: Her şey çalışıyor
- 🟡 **Yükleniyor**: Sistem başlatılıyor
- 🔴 **Veritabanı Yok**: Verileri işleyin

**🤖 Model Bilgisi**
- Model: Ollama Phi-3 Mini
- Vektör DB: Aktif/Pasif

**📚 Veri Yönetimi**
- **🔄 Verileri İşle / Güncelle**: Yeni veri eklediyseniz
- İlk kullanımda bu butona tıklayın!

**💬 Sohbet**
- **🗑️ Sohbeti Temizle**: Konuşma geçmişini sil
- **Mesaj Sayısı**: İstatistik

**ℹ️ Hakkında**
- Teknolojiler ve bilgi

#### Ana Ekran

**Chat Alanı**
- 👤 Mavi kenarlı: Sizin mesajlarınız
- 🎬 Yeşil kenarlı: Bot'un cevapları

**Soru Sorma**
- Alt kısımdaki input alanına sorunuzu yazın
- Enter'a basın

**Kaynak Belgeler**
- Her cevabın altında "📚 Kaynak Belgeler"
- Bot'un hangi film yorumlarından bilgi aldığını gösterir

### İlk Sorgunuz

1. **Sistem Hazır mı Kontrol Edin**
   - Sol panelde 🟢 "Sistem Hazır" yazmalı
   
2. **Soru Sorun!**
   ```
   En iyi aksiyon filmleri hangileri?
   ```

3. **Cevabı İnceleyin**
   - Bot IMDb yorumlarına göre cevap verecek
   - "📚 Kaynak Belgeler" ile kaynakları görebilirsiniz

### Örnek Sohbet Senaryosu

```
👤 Sen: Merhaba! Hangi filmler çok beğenilmiş?

🎬 Bot: Merhaba! IMDb veri setinde yüksek değerlendirme alan 
filmler arasında [film örnekleri]... [detaylı cevap]

👤 Sen: Korku filmi önerir misin?

🎬 Bot: Tabii! Korku kategorisinde şu filmler öne çıkıyor...

👤 Sen: Leonardo DiCaprio'nun iyi filmleri hangileri?

🎬 Bot: Leonardo DiCaprio'nun oynadığı ve yüksek puan alan 
filmler arasında...
```

### Kullanım İpuçları

✅ **İyi Sorular:**
- "En iyi aksiyon filmleri hangileri?"
- "Duygusal filmler önerir misin?"
- "Hangi filmler pozitif yorumlar almış?"
- "Komedi filmleri hakkında ne söyleniyor?"
- "Korku filmi öner"

❌ **Kötü Sorular:**
- "Bugün hava nasıl?" (veri setinde yok)
- "Saat kaç?" (chatbot'un amacı değil)
- Çok genel: "Film" (daha spesifik olun)

---

## 🔧 Sorun Giderme

### Sık Karşılaşılan Hatalar

#### 1. "Ollama bağlantı hatası"

**Çözüm:**
```bash
# Ollama servisini başlatın
ollama serve

# Başka bir terminalde kontrol edin
curl http://localhost:11434
```

#### 2. "Vektör veritabanı bulunamadı"

**Çözüm:**
```bash
# Streamlit arayüzünden "Verileri İşle" butonuna tıklayın
# VEYA
# Uygulama kapalıyken chroma_db klasörünü silin:
rmdir /s chroma_db  # Windows
rm -rf chroma_db    # Linux/Mac
```

#### 3. "ModuleNotFoundError"

**Çözüm:**
```bash
# Bağımlılıkları tekrar yükleyin
pip install -r requirements.txt

# Virtual environment aktif mi?
# (venv) yazısı komut satırında görünmeli
```

#### 4. "Port 8501 kullanımda"

**Çözüm:**
```bash
# Farklı port kullanın
streamlit run app.py --server.port 8502
```

#### 5. "Kaggle kimlik bilgileri bulunamadı"

**Çözüm:**
```bash
# kaggle.json dosyasının doğru yerde olduğundan emin olun
# Windows: C:\Users\YourUsername\.kaggle\kaggle.json
# Linux/Mac: ~/.kaggle/kaggle.json

# İçeriği kontrol edin
cat ~/.kaggle/kaggle.json  # Linux/Mac
type %USERPROFILE%\.kaggle\kaggle.json  # Windows
```

#### 6. "Embedding modeli indirilemiyor"

**Çözüm:**
- İnternet bağlantınızı kontrol edin
- İlk çalıştırmada HuggingFace'den model indirilir (~80MB)
- Proxy kullanıyorsanız ayarlarınızı kontrol edin

### Log Kontrolleri

Hata detaylarını görmek için:

```bash
# Terminal çıktısını kontrol edin
# Kırmızı HATA mesajları önemlidir

# Streamlit debug modu
streamlit run app.py --logger.level=debug

# Ollama logları
ollama serve --verbose
```

---

## ❓ Sık Sorulan Sorular

### 1. Tamamen ücretsiz mi?

✅ **Evet!** 
- Ollama: Ücretsiz ve lokal
- HuggingFace modeller: Ücretsiz
- Kaggle API: Ücretsiz
- ChromaDB: Ücretsiz

**Maliyet: $0**

### 2. İnternet gerekir mi?

**İlk kurulumda:**
- ✅ Model indirmek için (bir kez)
- ✅ Kaggle dataset indirmek için (bir kez)

**Kullanım sırasında:**
- ❌ Hayır! Tamamen offline çalışır

### 3. Kendi verilerimi ekleyebilir miyim?

✅ **Evet!** 

```bash
# 1. data/ klasörüne .txt dosyanızı ekleyin
# 2. Streamlit'te "Verileri İşle" butonuna tıklayın
```

### 4. Veritabanını nasıl sıfırlarım?

```bash
# chroma_db klasörünü silin
# Windows:
rmdir /s chroma_db

# Mac/Linux:
rm -rf chroma_db

# Streamlit'te "Verileri İşle" butonuna tıklayın
```

### 5. Daha hızlı yanıt için ne yapabilirim?

```python
# src/rag_pipeline.py dosyasında:

# k değerini düşürün (daha az context)
rag.create_qa_chain(k=2)  # varsayılan 4

# Temperature'ı düşürün
temperature=0.5  # varsayılan 0.7
```

### 6. Kaç film yorumu var?

**IMDb Dataset:**
- 50,000 film yorumu
- 25,000 pozitif
- 25,000 negatif
- Çeşitli film türleri

### 7. Başka Ollama modelleri kullanabilir miyim?

✅ **Evet!**

```python
# src/rag_pipeline.py dosyasında model değiştirin:

# Daha küçük (daha hızlı)
model="phi3:mini"

# Daha büyük (daha iyi)
model="llama3.2:3b"
model="gemma2:9b"
```

Önce modeli indirin:
```bash
ollama pull llama3.2:3b
```

### 8. CPU'da çalışır mı?

✅ **Evet!** Phi-3 Mini CPU'da iyi çalışır:
- **4GB RAM**: Yeterli
- **8GB RAM**: İdeal
- **CPU**: Modern herhangi bir CPU

### 9. Türkçe sorular sorabilir miyim?

✅ **Evet!** Ancak veri seti İngilizce:
- Türkçe soru sorabilirsiniz
- Bot Türkçe cevap verir
- Ama kaynak IMDb yorumları İngilizce

### 10. Production'a nasıl deploy ederim?

**Docker ile:**
```dockerfile
# Dockerfile oluşturun
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app.py"]
```

**Alternatifler:**
- Render.com
- Railway.app
- Kendi sunucunuz (Ollama ile)

---

## 📞 Destek

Sorun mu yaşıyorsunuz?

1. **README.md** dosyasını okuyun
2. **Bu kılavuzu** tekrar gözden geçirin
3. **GitHub Issues** kontrol edin
4. Yeni issue açın (hata detaylarıyla)

---

## 🎓 Öğrenme Kaynakları

**RAG Hakkında:**
- [RAG Paper (Original)](https://arxiv.org/abs/2005.11401)
- [LangChain RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)

**Ollama:**
- [Official Documentation](https://ollama.com/docs)
- [Model Library](https://ollama.com/library)

**Streamlit:**
- [Official Tutorial](https://docs.streamlit.io/library/get-started)
- [Gallery](https://streamlit.io/gallery)

**ChromaDB:**
- [Getting Started](https://docs.trychroma.com/getting-started)

---

## 🎯 Sonraki Adımlar

1. ✅ Kurulumu tamamladınız
2. ✅ IMDb dataset'i yüklediniz
3. ✅ Uygulamayı çalıştırdınız

**Şimdi:**
- 🎬 Film hakkında sorular sorun
- 📊 Farklı türlerde filmler keşfedin
- 🔧 Parametreleri deneyerek optimize edin
- 📚 Kendi verilerinizi ekleyin

---

**🎉 İyi kullanımlar! Keyifli film sohbetleri!**

*Akbank GenAI Bootcamp 🎓*
