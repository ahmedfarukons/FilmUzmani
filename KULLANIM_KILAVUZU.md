# 🎬 Film Gurusu Chatbot - Kullanım Kılavuzu

Bu kılavuz, Film Gurusu chatbot'unu adım adım nasıl kurup kullanacağınızı gösterir.

## 📋 İçindekiler
1. [Hızlı Başlangıç](#hızlı-başlangıç)
2. [Detaylı Kurulum](#detaylı-kurulum)
3. [İlk Çalıştırma](#ilk-çalıştırma)
4. [Web Arayüzü Kullanımı](#web-arayüzü-kullanımı)
5. [Sorun Giderme](#sorun-giderme)
6. [SSS](#sık-sorulan-sorular)

---

## 🚀 Hızlı Başlangıç

### 5 Dakikada Çalıştırın!

```bash
# 1. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 2. .env dosyası oluşturun
copy .env.example .env
# (Linux/Mac: cp .env.example .env)

# 3. .env dosyasını düzenleyin ve API key'inizi ekleyin
notepad .env
# GOOGLE_API_KEY=your_api_key_here

# 4. Veritabanını oluşturun
python setup.py

# 5. Uygulamayı başlatın
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

### Adım 2: Google API Key Alın

1. [Google AI Studio](https://makersuite.google.com/app/apikey)'ya gidin
2. Google hesabınızla giriş yapın
3. "Create API Key" butonuna tıklayın
4. API key'inizi kopyalayın (güvenli bir yerde saklayın!)

### Adım 3: Projeyi Hazırlayın

```bash
# Proje klasörüne gidin
cd film-gurusu-chatbot

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

### Adım 4: Environment Variables

`.env` dosyası oluşturun:

```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

`.env` dosyasını düzenleyin:

```
GOOGLE_API_KEY=AIzaSyB...your_actual_key_here...
```

⚠️ **Önemli**: API key'inizi kimseyle paylaşmayın!

---

## 🎬 İlk Çalıştırma

### Veritabanı Kurulumu

```bash
python setup.py
```

Script şunları yapacak:

1. **API Key Kontrolü**
   ```
   ✅ API key bulundu
   ```

2. **Veri Dosyası Kontrolü**
   ```
   ✅ 1 adet veri dosyası bulundu
   ```

3. **Onay İstemi**
   ```
   Devam etmek istiyor musunuz? (E/H):
   ```
   `E` yazıp Enter'a basın.

4. **Veri İşleme**
   ```
   📊 ADIM 1: Veri İşleme (Chunking)
   ✓ 50 chunk oluşturuldu
   ```

5. **Vektör Veritabanı Oluşturma**
   ```
   💾 ADIM 3: Vektör Veritabanı Oluşturuluyor
   ✓ Vektör veritabanı oluşturuldu ve kaydedildi
   ```

6. **Test Sorgusu**
   ```
   🧪 Test Sorgusu Çalıştırılıyor...
   Soru: Hangi filmler hakkında eleştiri var?
   Cevap: [AI'dan gelen cevap]
   ```

✅ Başarılı! Artık uygulamayı çalıştırabilirsiniz.

---

## 💻 Web Arayüzü Kullanımı

### Uygulamayı Başlatın

```bash
streamlit run app.py
```

Tarayıcı otomatik açılacak. Açılmazsa: `http://localhost:8501`

### Arayüz Tanıtımı

#### Sol Panel (Sidebar)

**⚙️ Ayarlar**
- **Google API Key**: API key'inizi girin (güvenlik için gizli)
- **🚀 RAG Sistemini Başlat**: Sistemi aktif hale getirin

**📚 Veri Yönetimi**
- **🔄 Verileri İşle**: Yeni veri eklediyseniz veritabanını güncelleyin

**💬 Sohbet**
- **🗑️ Sohbeti Temizle**: Konuşma geçmişini sıfırlayın

**📊 İstatistikler**
- Mesaj sayısı
- Veritabanı durumu

**ℹ️ Hakkında**
- Proje bilgileri

#### Ana Ekran

**Chat Alanı**
- 👤 Mavi kenarlı: Sizin mesajlarınız
- 🎬 Yeşil kenarlı: Bot'un cevapları

**Soru Sorma**
- Alt kısımdaki input alanına sorunuzu yazın
- Enter veya ▶ butonuna basın

**Kaynak Belgeler**
- Her cevabın altında "📚 Kaynak Belgeler" açılır menüsü
- Bot'un hangi kaynaklardan bilgi aldığını gösterir

### İlk Sorgunuz

1. **API Key Girin**
   - Sol panelden API key'inizi yapıştırın

2. **RAG Sistemini Başlatın**
   - "🚀 RAG Sistemini Başlat" butonuna tıklayın
   - ✅ "RAG sistemi aktif" mesajını bekleyin

3. **Soru Sorun!**
   ```
   Christopher Nolan'ın hangi filmleri hakkında eleştiri var?
   ```

4. **Cevabı İnceleyin**
   - Bot detaylı bir cevap verecek
   - "📚 Kaynak Belgeler" açıp kaynakları görebilirsiniz

### Örnek Sohbet Senaryosu

```
👤 Sen: Merhaba! Bana Inception hakkında bilgi verir misin?

🎬 Bot: Merhaba! Tabii ki. "Inception" (Başlangıç), Christopher 
Nolan'ın 2010 yapımı bilim kurgu걸작... [detaylı cevap]

👤 Sen: Bu filmin puanı neydi?

🎬 Bot: "Inception" film eleştirisinde 9/10 puan almıştır...

👤 Sen: Christopher Nolan'ın başka hangi filmleri var burada?

🎬 Bot: Veri setimizde Christopher Nolan'ın şu filmleri bulunuyor:
1. Inception (2010) - 9/10
2. The Dark Knight (2008) - 9.5/10
...
```

### Kullanım İpuçları

✅ **İyi Sorular:**
- "Hangi filmler en yüksek puan almış?"
- "Duygusal filmler önerir misin?"
- "Parasite filminin konusu ne?"
- "Leonardo DiCaprio'nun oynadığı filmler hangileri?"

❌ **Kötü Sorular:**
- "Bugün hava nasıl?" (veri setinde yok)
- "Saat kaç?" (chatbot'un amacı değil)
- Çok genel: "Film" (daha spesifik olun)

---

## 🔧 Sorun Giderme

### Sık Karşılaşılan Hatalar

#### 1. "GOOGLE_API_KEY bulunamadı"

**Çözüm:**
```bash
# .env dosyasını kontrol edin
notepad .env

# Şöyle görünmeli:
GOOGLE_API_KEY=AIzaSyB...

# Boşluk olmamalı, tırnak olmamalı!
```

#### 2. "Vektör veritabanı bulunamadı"

**Çözüm:**
```bash
# Setup'ı tekrar çalıştırın
python setup.py
```

#### 3. "ModuleNotFoundError"

**Çözüm:**
```bash
# Bağımlılıkları tekrar yükleyin
pip install -r requirements.txt

# Virtual environment aktif mi kontrol edin
# (venv) yazısı komut satırında görünmeli
```

#### 4. "Port 8501 kullanımda"

**Çözüm:**
```bash
# Farklı port kullanın
streamlit run app.py --server.port 8502
```

#### 5. "API Rate Limit Exceeded"

**Çözüm:**
- 60 saniye bekleyin (Gemini free tier limiti)
- Daha az sık soru sorun
- Paid plan'e geçin

### Log Kontrolleri

Hata detaylarını görmek için:

```bash
# Terminal çıktısını kontrol edin
# Kırmızı HATA mesajları önemlidir

# Streamlit logları
streamlit run app.py --logger.level=debug
```

---

## ❓ Sık Sorulan Sorular

### 1. API key ücretsiz mi?

✅ **Evet!** Google Gemini API'nin ücretsiz bir tier'ı var:
- 60 request/dakika
- Günlük limit var ama genellikle yeterli

### 2. Kendi verilerimi ekleyebilir miyim?

✅ **Evet!** 

```bash
# 1. data/ klasörüne .txt dosyanızı ekleyin
# 2. Setup'ı tekrar çalıştırın
python setup.py
```

### 3. İnternetsiz çalışır mı?

❌ **Hayır.** Gemini API internet bağlantısı gerektirir.

### 4. Veritabanını nasıl sıfırlarım?

```bash
# chroma_db klasörünü silin
# Windows:
rmdir /s chroma_db

# Mac/Linux:
rm -rf chroma_db

# Sonra tekrar oluşturun
python setup.py
```

### 5. Daha hızlı yanıt almak için ne yapabilirim?

```python
# src/rag_pipeline.py dosyasında:
# k değerini düşürün (daha az context)
rag.create_qa_chain(k=2)  # varsayılan 4

# Temperature'ı düşürün (daha deterministik)
temperature=0.3  # varsayılan 0.7
```

### 6. Kaç film eleştirisi var?

Örnek veri setinde **13 film eleştirisi** var:
- The Shawshank Redemption
- The Godfather
- Parasite
- Inception
- Pulp Fiction
- Spirited Away
- The Dark Knight
- Amélie
- Fight Club
- City of God
- Eternal Sunshine of the Spotless Mind
- 12 Angry Men
- Pan's Labyrinth

### 7. Türkçe dışında dil desteği var mı?

✅ **Evet!** Gemini multi-lingual. İngilizce soru sorabilirsiniz:

```
"What are the best rated movies in the database?"
```

### 8. Production'a nasıl deploy ederim?

**Streamlit Cloud (Ücretsiz):**
1. GitHub'a push yapın
2. [share.streamlit.io](https://share.streamlit.io)'ya gidin
3. Repository'yi seçin
4. Secrets'a API key ekleyin
5. Deploy!

**Alternatifler:**
- Heroku
- AWS
- Google Cloud Run
- Azure

---

## 📞 Destek

Sorun mu yaşıyorsunuz?

1. **README.md** dosyasını okuyun
2. **GitHub Issues** kontrol edin
3. Yeni issue açın (hata detaylarıyla)
4. Email: your.email@example.com

---

## 🎓 Öğrenme Kaynakları

**RAG Hakkında:**
- [RAG Paper (Original)](https://arxiv.org/abs/2005.11401)
- [LangChain RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)

**Streamlit:**
- [Official Tutorial](https://docs.streamlit.io/library/get-started)
- [Gallery](https://streamlit.io/gallery)

**Gemini API:**
- [Google AI Documentation](https://ai.google.dev/)
- [Cookbook](https://github.com/google-gemini/cookbook)

---

**🎉 İyi kullanımlar! Keyifli film sohbetleri!**

*Akbank GenAI Bootcamp 🎓*

