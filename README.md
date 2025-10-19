# 🎬 Film Uzmani

Türkçe/English below ⬇️

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-ff4b4b)
![LangChain](https://img.shields.io/badge/LangChain-0.1+-00b16a)
![FAISS](https://img.shields.io/badge/VectorDB-FAISS-3c3c3c)
![Transformers](https://img.shields.io/badge/Embeddings-Transformers-yellow)
![LLM](https://img.shields.io/badge/LLM-Gemini%20%7C%20Ollama-8a2be2)

## 🇹🇷 Türkçe

### Ne yapar?
- RAG: Sorgunu FAISS’te arar, en alakalı chunk’ları toplar, LLM ile yanıtlar.
- Çeşitlilik: MMR retriever (k=6, fetch_k dinamik) ile farklı film örnekleri.
- Kaynaklar: Yanıtın altında kullanılan dokümanları gösterir.

### ⚙️ Kurulum

1) Python ve bağımlılıklar:
```
pip install -r requirements.txt
```
2) Model seçimi:
```
GEMINI_API_KEY=...  # veya GOOGLE_API_KEY
```
   - Gemini: `.env` içine `GEMINI_API_KEY=...` (veya `GOOGLE_API_KEY`)
   - Ollama: `ollama pull phi3:mini` (servis: `http://localhost:11434`)
3) Veri: `data/` içinde `imdb_50k_reviews.txt` hazır. Kendi `.txt/.csv/.json` dosyalarını ekleyebilirsin.

### 🚀 Çalıştırma
```
python -m streamlit run app.py
```

### 🖼️ Ekran Görüntüsü
![Uygulama Ekranı](assets/screenshot.png)

### 🗂️ Veri Kaynağı
- [IMDb 50K Movie Reviews – Kaggle](https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews)
- Bu proje, söz konusu veri setinden türetilen `data/imdb_50k_reviews.txt` dosyasını kullanır.

### 🎥 Demo Video
- [YouTube Demo](https://youtu.be/9-0L8U61Pjc)

### 📖 Kullanım Kılavuzu (Özet)
1) Sol panel → “Verileri İşle / Güncelle” ile FAISS oluşturun/güncelleyin.
2) Üstte model seçimi (Gemini veya Ollama). Gemini için .env’de API key olmalı.
3) Ana alandaki sohbet kutusuna sorunuzu yazın; yanıt ve “Kaynak Belgeler”i inceleyin.
4) Çeşitlilik için soruyu yönlendirin (örn. “farklı türlerden 3 film öner”).

### 📁 Proje Yapısı
```
app.py
src/
  data_processor.py
  rag_pipeline.py
data/
faiss_db/
scripts/
requirements.txt
```

## 🇬🇧 English

### 🎯 About
- RAG: Retrieve top chunks from FAISS, answer with LLM (Gemini/Ollama).
- Diversity: MMR retriever (k=6) to surface varied film examples.
- Sources: Shows documents used for the answer.

### ⚙️ Setup
```
pip install -r requirements.txt
# optional: Gemini
# .env -> GEMINI_API_KEY=...  (or GOOGLE_API_KEY)
# optional: local LLM
ollama pull phi3:mini
```

### 🚀 Run
```
python -m streamlit run app.py
```

### 🖼️ Screenshot
![App Screenshot](assets/screenshot.png)

### 🗂️ Dataset Source
- [IMDb 50K Movie Reviews – Kaggle](https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews)
- The app uses a derived file `data/imdb_50k_reviews.txt` built from that dataset.

### 🎥 Demo Video
- [YouTube Demo](https://youtu.be/9-0L8U61Pjc)

### 📖 User Guide (Quick)
1) Sidebar → “Process / Update Data” to build/update FAISS.
2) Select model (Gemini or Ollama). Gemini requires API key in .env.
3) Ask in the chat box; review answer and “Source Documents”.
4) For diversity, steer the prompt (e.g., “3 films from different genres”).

### 💡 Notes
- Indexing can take time on large data.
- Increase k for broader coverage; prompt with “from different genres”.
- CSV/JSON title metadata enables a “unique films” metric.

---
MIT License. Author: Ahmed Faruk Onus.
