# 🎬 Film Gurusu Chatbot

**Akbank GenAI Bootcamp - Yeni Nesil Proje Kampı**

RAG (Retrieval-Augmented Generation) teknolojisi kullanan, film eleştirileri üzerine akıllı sohbet edebilen chatbot uygulaması.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red)
![LangChain](https://img.shields.io/badge/LangChain-0.1.9-green)
![Ollama](https://img.shields.io/badge/Ollama-Lokal-purple)
![Groq](https://img.shields.io/badge/Groq-Llama%203.2-orange)

## 📋 İçindekiler

- [Proje Hakkında](#proje-hakkında)
- [Özellikler](#özellikler)
- [Teknolojiler](#teknolojiler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Proje Yapısı](#proje-yapısı)
- [RAG Mimarisi](#rag-mimarisi)
- [Ekran Görüntüleri](#ekran-görüntüleri)
- [Geliştirme](#geliştirme)
- [Katkıda Bulunma](#katkıda-bulunma)

## 🎯 Proje Hakkında

Film Gurusu, kullanıcıların film eleştirileri hakkında sorular sorabileceği ve detaylı, bağlama dayalı cevaplar alabileceği bir yapay zeka chatbot'udur. Proje, RAG (Retrieval-Augmented Generation) mimarisini kullanarak, önce ilgili bilgileri bir vektör veritabanından alır, sonra bu bilgileri kullanarak **Ollama (tamamen lokal)** veya **Groq (Llama 3.2 90B)** ile zenginleştirilmiş cevaplar üretir.

### Projenin Amacı

Bu proje, modern NLP ve LLM teknolojilerini kullanarak:
- Film eleştirilerinden oluşan bir bilgi havuzunu anlamsal olarak indexleme
- Kullanıcı sorularına bağlam-farkındalı cevaplar verme
- RAG mimarisinin pratik bir uygulamasını gösterme
- Web tabanlı kullanıcı dostu bir arayüz sunma

## ✨ Özellikler

- 🤖 **RAG Tabanlı Cevaplama**: Retrieval-Augmented Generation ile akıllı cevaplar
- 💬 **Doğal Dil İşleme**: Türkçe dilinde doğal konuşma desteği
- 🎨 **Modern Web Arayüzü**: Streamlit ile geliştirilmiş kullanıcı dostu tasarım
- 📚 **Kaynak Gösterimi**: Cevapların hangi kaynaklardan geldiğini gösterme
- 🔍 **Semantik Arama**: ChromaDB ile anlamsal benzerlik araması
- ⚡ **Hızlı Yanıt**: Optimize edilmiş vektör araması ve caching
- 📊 **Chunk Yönetimi**: Akıllı metin bölümleme (chunking) sistemi
- 🔐 **Güvenli API Yönetimi**: Environment variables ile güvenli yapılandırma

## 🛠️ Teknolojiler

### Backend
- **Python 3.8+**: Ana programlama dili
- **LangChain**: RAG pipeline ve zincir yönetimi
- **Ollama (Phi-3 Mini)**: Lokal LLM - API key gerektirmez
- **Groq (Llama 3.2 90B)**: Cloud LLM - Ücretsiz ve çok hızlı
- **ChromaDB**: Vektör veritabanı
- **Transformers**: Custom lokal embedding (all-MiniLM-L6-v2)

### Frontend
- **Streamlit**: Web arayüzü framework'ü
- **Custom CSS**: Özel tasarım ve stilizasyon

### Diğer
- **python-dotenv**: Environment variables yönetimi
- **PyPDF2**: PDF okuma desteği (opsiyonel)
- **pandas**: Veri manipülasyonu

## 📦 Kurulum

### Gereksinimler

- Python 3.8 veya üzeri
- **Seçenek 1 (Önerilen):** Ollama kurulu ([buradan indirin](https://ollama.com/download)) - Tamamen ücretsiz ve lokal
- **Seçenek 2:** Groq API Key ([buradan alın](https://console.groq.com/keys)) - Ücretsiz kuota
- 4GB+ RAM (ChromaDB ve model için)

### Adım 1: Projeyi Klonlayın

```bash
git clone https://github.com/ahmedfarukons/FilmUzmani.git
cd FilmUzmani
```

### Adım 2: Virtual Environment Oluşturun (Önerilen)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Adım 3: Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### Adım 4: Model Seçimi

**Seçenek 1: Ollama (Önerilen - Tamamen Ücretsiz & Lokal)**

1. Ollama'yı indirin: https://ollama.com/download
2. Phi-3 modelini çekin:
```bash
ollama pull phi3:mini
```
3. Ollama servisini başlatın:
```bash
ollama serve
```
4. Artık hazırsınız! API key gerekmez.

**Seçenek 2: Groq (Cloud - Ücretsiz & Hızlı)**

1. `.env` dosyası oluşturun ve Groq API key'inizi ekleyin:
```bash
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```
2. Ücretsiz API key almak için: https://console.groq.com/keys

### Adım 5: Veritabanını Oluşturun

İlk kez çalıştırmadan önce, vektör veritabanını oluşturmanız gerekir:

```bash
python setup.py
```

Bu script:
- ✅ API key kontrolü yapacak
- ✅ Veri dosyalarını kontrol edecek
- ✅ Metinleri chunk'lara böler
- ✅ Embedding'leri oluşturacak
- ✅ ChromaDB veritabanını kuracak
- ✅ Bir test sorgusu çalıştıracak

## 🚀 Kullanım

### Web Arayüzünü Başlatma

```bash
streamlit run app.py
```

Tarayıcınızda otomatik olarak `http://localhost:8501` adresi açılacaktır.

### İlk Kullanım

1. **Model Seçin**: Sol panelden "ollama" veya "groq" seçin
2. **RAG Sistemi Başlatın**: "🚀 RAG Sistemini Başlat" butonuna tıklayın
   - İlk kullanımda "🔄 Verileri İşle" butonuna tıklayın (embedding modeli indirilir)
3. **Soru Sorun**: Chat alanından filmler hakkında sorular sorun!

### Örnek Sorular

```
🎬 Christopher Nolan'ın hangi filmleri hakkında eleştiri var?
🎬 En yüksek puan alan filmler hangileri?
🎬 Parasite filmi hakkında ne düşünülüyor?
🎬 Duygusal ve derin bir film önerir misin?
🎬 Sosyal eleştiri içeren filmler hangileri?
🎬 Tim Robbins hangi filmlerde oynadı?
```

## 📁 Proje Yapısı

```
film-gurusu-chatbot/
│
├── app.py                      # Ana Streamlit web uygulaması
├── setup.py                    # Kurulum ve veri işleme scripti
├── requirements.txt            # Python bağımlılıkları
├── .env.example               # Environment variables şablonu
├── .gitignore                 # Git ignore dosyası
├── README.md                  # Proje dokümantasyonu
│
├── src/                       # Kaynak kod modülleri
│   ├── __init__.py
│   ├── data_processor.py      # Veri yükleme ve chunking
│   └── rag_pipeline.py        # RAG pipeline ve QA sistemi
│
├── data/                      # Film eleştirileri veri seti
│   └── sample_reviews.txt     # Örnek eleştiriler
│
└── chroma_db/                 # ChromaDB vektör veritabanı (otomatik oluşur)
    └── ...
```

## 🏗️ RAG Mimarisi

### 1. Veri Hazırlama (Data Processing)

```python
DataProcessor → Metin Dosyaları → Chunking → Document Nesneleri
```

- **Chunk Size**: 1000 karakter
- **Chunk Overlap**: 200 karakter
- **Separators**: Paragraf, cümle, kelime bazlı ayırma

### 2. Embedding ve Vektörleştirme

```python
Documents → Custom Transformers (all-MiniLM-L6-v2) → Vektörler → ChromaDB
```

- **Model**: `sentence-transformers/all-MiniLM-L6-v2` (Lokal)
- **Vektör Boyutu**: 384 dimensions
- **Veritabanı**: ChromaDB (persist)

### 3. Retrieval (Bilgi Getirme)

```python
Kullanıcı Sorusu → Embedding → Similarity Search → Top-K Documents
```

- **Arama Tipi**: Similarity Search
- **K Değeri**: 4 (en benzer 4 chunk)
- **Similarity Metric**: Cosine similarity

### 4. Generation (Cevap Üretme)

```python
Soru + Retrieved Context → Ollama/Groq → Zenginleştirilmiş Cevap
```

- **Ollama Model**: Phi-3 Mini (3.8B) - Lokal
- **Groq Model**: Llama 3.2 90B - Cloud
- **Temperature**: 0.7
- **Chain Type**: Stuff (tüm context birlikte gönderilir)

### RAG Pipeline Akışı

```
┌─────────────────┐
│  Kullanıcı      │
│  Sorusu         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Embedding      │
│  (Soru → Vektör)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  ChromaDB       │
│  Similarity     │
│  Search         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Top-K          │
│  Dokümanlarsı   │
│  Getir          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Prompt         │
│  Oluştur        │
│  (Soru+Context) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Ollama/Groq    │
│  LLM            │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Zenginleştiril-│
│  miş Cevap      │
└─────────────────┘
```

## 🎨 Ekran Görüntüleri

### Ana Ekran
Web arayüzü modern, karanlık tema ile geliştirilmiştir ve kullanıcı dostu bir deneyim sunar.

**Özellikler:**
- 💬 Gerçek zamanlı chat arayüzü
- 📚 Kaynak belge gösterimi
- 📊 İstatistikler paneli
- ⚙️ Kolay yapılandırma

## 🔧 Geliştirme

### Yeni Veri Ekleme

1. Film eleştirilerinizi `data/` klasörüne `.txt` formatında ekleyin
2. Setup scriptini yeniden çalıştırın:
```bash
python setup.py
```

### Chunk Parametrelerini Ayarlama

`src/data_processor.py` dosyasında:

```python
processor = DataProcessor(
    chunk_size=1000,      # Chunk boyutu
    chunk_overlap=200     # Overlap miktarı
)
```

### Retrieval Parametrelerini Ayarlama

`src/rag_pipeline.py` dosyasında:

```python
rag.create_qa_chain(k=4)  # Döndürülecek chunk sayısı
```

### LLM Parametrelerini Ayarlama

**Ollama için:**
```python
self.llm = ChatOllama(
    model="phi3:mini",
    temperature=0.7,      # Yaratıcılık seviyesi (0.0-1.0)
    base_url="http://localhost:11434"
)
```

**Groq için:**
```python
self.llm = ChatGroq(
    model="llama-3.2-90b-text-preview",
    temperature=0.7,
    max_tokens=2048
)
```

## 📝 Notlar

### Performans İpuçları

- **Chunk Size**: Çok küçük chunk'lar → fazla context kaybı, Çok büyük chunk'lar → ilgisiz bilgi
- **Overlap**: Cümle bütünlüğünü korumak için önerilir
- **K Değeri**: Fazla chunk → yavaş yanıt + maliyetli, Az chunk → bilgi eksikliği

### API Maliyetleri

- **Ollama**: Tamamen ücretsiz (lokal çalışır, internet gerekmez)
- **Groq**: Ücretsiz tier mevcut (hızlı yanıt)
- **Embedding**: Lokal model, internet gerekmez, ücretsiz

### Veri Gizliliği

- API key'leri asla commit etmeyin
- `.env` dosyası `.gitignore`'da olmalı
- Hassas veriler için kendi sunucunuzu kullanın

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen şu adımları takip edin:

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'inizi push edin (`git push origin feature/AmazingFeature`)
5. Pull Request açın

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 👥 İletişim

**Proje Sahibi**: Ahmed Faruk Öns
- GitHub: [@ahmedfarukons](https://github.com/ahmedfarukons)

**Proje Linki**: [https://github.com/ahmedfarukons/FilmUzmani](https://github.com/ahmedfarukons/FilmUzmani)

## 🙏 Teşekkürler

- **Akbank GenAI Bootcamp** - Eğitim ve destek için
- **Ollama** - Lokal LLM desteği için
- **Groq** - Hızlı ve ücretsiz cloud LLM için
- **LangChain** - RAG framework için
- **Streamlit** - Web framework için
- **ChromaDB** - Vektör veritabanı için
- **HuggingFace** - Transformers ve model desteği için

---

**⭐ Projeyi beğendiyseniz yıldız vermeyi unutmayın!**

---

## 📚 Kaynaklar

- [LangChain Documentation](https://python.langchain.com/)
- [Ollama Documentation](https://ollama.com/)
- [Groq Documentation](https://console.groq.com/docs)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [RAG Papers](https://arxiv.org/abs/2005.11401)

---

*Bu proje Akbank GenAI Bootcamp kapsamında geliştirilmiştir. 🎓*

