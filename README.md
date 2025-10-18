# 🎬 Film Gurusu Chatbot

**Akbank GenAI Bootcamp - Yeni Nesil Proje Kampı**

RAG (Retrieval-Augmented Generation) teknolojisi kullanan, film yorumları üzerine akıllı sohbet edebilen **tamamen lokal** chatbot uygulaması.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red)
![LangChain](https://img.shields.io/badge/LangChain-0.1.9-green)
![Ollama](https://img.shields.io/badge/Ollama-Lokal-purple)

## 📋 İçindekiler

- [Proje Hakkında](#proje-hakkında)
- [Özellikler](#özellikler)
- [Teknolojiler](#teknolojiler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [IMDb Dataset](#imdb-dataset)
- [Proje Yapısı](#proje-yapısı)
- [RAG Mimarisi](#rag-mimarisi)

## 🎯 Proje Hakkında

Film Gurusu, kullanıcıların film yorumları hakkında sorular sorabileceği ve detaylı, bağlama dayalı cevaplar alabileceği bir yapay zeka chatbot'udur. Proje, RAG (Retrieval-Augmented Generation) mimarisini kullanarak, önce ilgili bilgileri bir vektör veritabanından alır, sonra bu bilgileri kullanarak **Ollama (Phi-3 Mini)** ile zenginleştirilmiş cevaplar üretir.

### 🔥 Neden Tamamen Lokal?

- ✅ **Ücretsiz**: API key gerekmez, maliyet yok
- ✅ **Hızlı**: Network latency yok
- ✅ **Güvenli**: Verileriniz sunucunuza çıkmaz
- ✅ **Offline**: İnternet bağlantısı gerekmez
- ✅ **Sınırsız**: Sorgu limiti yok

## ✨ Özellikler

- 🤖 **RAG Tabanlı Cevaplama**: Retrieval-Augmented Generation ile akıllı cevaplar
- 🏠 **Tamamen Lokal**: Ollama ile internet gerektirmeden çalışır
- 💬 **Doğal Dil İşleme**: Türkçe ve İngilizce doğal konuşma desteği
- 🎨 **Modern Web Arayüzü**: Streamlit ile kullanıcı dostu tasarım
- 📚 **Kaynak Gösterimi**: Cevapların hangi kaynaklardan geldiğini gösterme
- 🔍 **Semantik Arama**: ChromaDB ile anlamsal benzerlik araması
- ⚡ **Otomatik Başlatma**: Uygulamayı açtığınızda sistem hazır
- 📊 **50K IMDb Yorumu**: Zengin ve çeşitli film veri seti

## 🛠️ Teknolojiler

### Backend
- **Python 3.8+**: Ana programlama dili
- **LangChain**: RAG pipeline ve zincir yönetimi
- **Ollama (Phi-3 Mini 3.8B)**: Lokal LLM - API key gerektirmez
- **ChromaDB**: Vektör veritabanı
- **Transformers**: Lokal embedding (all-MiniLM-L6-v2)

### Frontend
- **Streamlit**: Web arayüzü framework'ü
- **Custom CSS**: Özel tasarım ve stilizasyon

### Dataset
- **IMDb 50K Reviews**: Kaggle'dan public dataset
- **Pandas**: Veri işleme

## 📦 Kurulum

### Gereksinimler

- Python 3.8 veya üzeri
- Ollama ([buradan indirin](https://ollama.com/download))
- 4GB+ RAM (ChromaDB ve model için)
- Kaggle hesabı (dataset için)

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

### Adım 4: Ollama Kurulumu

1. Ollama'yı indirin: https://ollama.com/download
2. Phi-3 modelini çekin:
```bash
ollama pull phi3:mini
```
3. Ollama servisini başlatın:
```bash
ollama serve
```

### Adım 5: Kaggle API Yapılandırması

1. Kaggle hesabınızdan API token indirin:
   - https://www.kaggle.com/account
   - "Create New API Token" butonuna tıklayın
2. `kaggle.json` dosyasını şu konuma koyun:
   - **Windows**: `C:\Users\YourUsername\.kaggle\kaggle.json`
   - **Linux/Mac**: `~/.kaggle/kaggle.json`

### Adım 6: IMDb Dataset'i İndirin ve İşleyin

```bash
# Dataset'i indir (50K IMDb yorumu)
python scripts/download_imdb_dataset.py

# Dataset'i işle ve metin dosyalarına dönüştür
python scripts/process_imdb_dataset.py
```

## 🚀 Kullanım

### Web Arayüzünü Başlatma

```bash
streamlit run app.py
```

Tarayıcınızda otomatik olarak `http://localhost:8501` adresi açılacaktır.

### İlk Kullanım

1. **Sistem Otomatik Başlar**: Uygulama açıldığında RAG sistemi otomatik olarak hazırlanır
2. **Veritabanı Yoksa**: Sol panelden "🔄 Verileri İşle / Güncelle" butonuna tıklayın
3. **Soru Sorun**: Chat alanından filmler hakkında sorular sorun!

### Örnek Sorular

```
🎬 En iyi aksiyon filmleri hangileri?
🎬 Duygusal ve derin filmler öner
🎬 Komedi filmleri hakkında ne söyleniyor?
🎬 Korku filmi önerisi
🎬 Hangi filmler çok beğenilmiş?
🎬 Leonardo DiCaprio'nun iyi filmleri
```

## 📊 IMDb Dataset

### Dataset Hakkında

- **Kaynak**: [IMDb Dataset of 50K Movie Reviews - Kaggle](https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews)
- **Boyut**: 50,000 film yorumu
- **Dil**: İngilizce
- **Sentiment**: 25K pozitif, 25K negatif yorum
- **Format**: Her yorum ayrı chunk'larda, semantik arama için optimize edilmiş

### Dataset Yapısı

İndirilen ve işlenen dataset şu formattadır:

```
data/
├── backup/
│   └── sample_reviews_backup.txt    # Eski örnek veriler
├── imdb_reviews_01.txt              # 5000 yorum
├── imdb_reviews_02.txt              # 5000 yorum
├── ...
└── imdb_reviews_10.txt              # 5000 yorum
```

Her dosya şu formatta yorumlar içerir:

```
Film Yorumu #1
--------------------------------------------------------------------------------
Değerlendirme: positive/negative

[Yorum metni burada]

================================================================================
```

## 📁 Proje Yapısı

```
FilmUzmani/
│
├── app.py                          # Ana Streamlit web uygulaması
├── requirements.txt                # Python bağımlılıkları
├── README.md                       # Proje dokümantasyonu
│
├── src/                            # Kaynak kod modülleri
│   ├── __init__.py
│   ├── data_processor.py           # Veri yükleme ve chunking
│   ├── rag_pipeline.py             # RAG pipeline (sadece Ollama)
│   └── backup/
│       └── multi_provider_rag_pipeline.py  # Eski multi-provider versiyonu
│
├── scripts/                        # Yardımcı scriptler
│   ├── download_imdb_dataset.py    # Kaggle'dan dataset indir
│   └── process_imdb_dataset.py     # CSV'yi metin dosyalarına dönüştür
│
├── data/                           # Film yorumları
│   ├── imdb_reviews_*.txt          # İşlenmiş IMDb yorumları
│   └── backup/                     # Eski veriler
│
└── chroma_db/                      # ChromaDB vektör veritabanı (otomatik)
```

## 🏗️ RAG Mimarisi

### 1. Veri Hazırlama

```
IMDb CSV → Parse → Text Files → Chunking → Documents
```

- **Chunk Size**: 1000 karakter
- **Chunk Overlap**: 200 karakter
- **Separators**: Paragraf, cümle, kelime bazlı

### 2. Embedding ve Vektörleştirme

```
Documents → Transformers (all-MiniLM-L6-v2) → Vectors → ChromaDB
```

- **Model**: sentence-transformers/all-MiniLM-L6-v2 (Lokal)
- **Vektör Boyutu**: 384 dimensions
- **Veritabanı**: ChromaDB (persistent)

### 3. Retrieval (Bilgi Getirme)

```
User Query → Embedding → Similarity Search → Top-4 Documents
```

- **Arama Tipi**: Cosine similarity
- **K Değeri**: 4 (en benzer 4 chunk)

### 4. Generation (Cevap Üretme)

```
Query + Context → Ollama Phi-3 Mini → Enriched Answer
```

- **Model**: Phi-3 Mini (3.8B parameters)
- **Temperature**: 0.7
- **Lokal**: Tamamen offline çalışır

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
│  (Lokal)        │
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
│  Top-4          │
│  Chunks         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Ollama         │
│  Phi-3 Mini     │
│  (Lokal)        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Cevap          │
└─────────────────┘
```

## 🔧 Geliştirme

### Yeni Veri Ekleme

1. Film yorumlarınızı `data/` klasörüne `.txt` formatında ekleyin
2. Uygulamada "🔄 Verileri İşle / Güncelle" butonuna tıklayın

### Parametreleri Ayarlama

**Chunk Boyutu** (`src/data_processor.py`):
```python
processor = DataProcessor(chunk_size=1000, chunk_overlap=200)
```

**Retrieval** (`src/rag_pipeline.py`):
```python
rag.create_qa_chain(k=4)  # Döndürülecek chunk sayısı
```

**LLM** (`src/rag_pipeline.py`):
```python
self.llm = ChatOllama(
    model="phi3:mini",
    temperature=0.7,  # 0.0-1.0 arası
    base_url="http://localhost:11434"
)
```

## 📝 Notlar

### Performans

- **CPU**: Phi-3 Mini CPU'da iyi çalışır
- **RAM**: Minimum 4GB, 8GB önerilir
- **Disk**: ~10GB (model + embeddings + dataset)

### Alternatif Ollama Modelleri

```bash
# Daha küçük (daha hızlı)
ollama pull phi3:mini

# Daha büyük (daha iyi)
ollama pull llama3.2:3b
ollama pull gemma2:9b
```

### Veri Gizliliği

- ✅ Tüm işlemler lokal
- ✅ API key gerekmez
- ✅ Veriler sunucunuza çıkmaz
- ✅ Tamamen offline çalışır

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz!

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/Feature`)
3. Commit edin (`git commit -m 'Add Feature'`)
4. Push edin (`git push origin feature/Feature`)
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
- **LangChain** - RAG framework için
- **Streamlit** - Web framework için
- **ChromaDB** - Vektör veritabanı için
- **HuggingFace** - Transformers desteği için
- **Kaggle** - IMDb dataset için

---

**⭐ Projeyi beğendiyseniz yıldız vermeyi unutmayın!**

---

## 📚 Kaynaklar

- [LangChain Documentation](https://python.langchain.com/)
- [Ollama Documentation](https://ollama.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [RAG Papers](https://arxiv.org/abs/2005.11401)

---

*Bu proje Akbank GenAI Bootcamp kapsamında geliştirilmiştir. 🎓*
