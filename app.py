"""
Film Gurusu Chatbot - Streamlit Web Arayüzü
Akbank GenAI Bootcamp Projesi
"""
import os
import streamlit as st
from dotenv import load_dotenv
from src.data_processor import DataProcessor
from src.rag_pipeline import RAGPipeline

# Sayfa yapılandırması
st.set_page_config(
    page_title="🎬 Film Uzmani",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS ile özel stil
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stTextInput > div > div > input {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #2b313e;
        border-left: 5px solid #4a9eff;
    }
    .bot-message {
        background-color: #1e2530;
        border-left: 5px solid #00d4aa;
    }
    .stButton > button {
        background-color: #00d4aa;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 2rem;
    }
    .stButton > button:hover {
        background-color: #00b894;
    }
    h1 {
        color: #00d4aa;
        text-align: center;
        font-size: 3rem;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        color: #888;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)


def initialize_session_state():
    """Session state değişkenlerini başlatır"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'rag_pipeline' not in st.session_state:
        st.session_state.rag_pipeline = None
    
    if 'vectorstore_loaded' not in st.session_state:
        st.session_state.vectorstore_loaded = False
    
    if 'api_key_configured' not in st.session_state:
        st.session_state.api_key_configured = False
    
    if 'model_provider' not in st.session_state:
        st.session_state.model_provider = "ollama"


def load_rag_pipeline(model_provider: str, groq_api_key: str = None):
    """RAG Pipeline'ı yükler"""
    try:
        with st.spinner("🔄 RAG sistemi yükleniyor..."):
            # Model provider'a göre pipeline oluştur
            rag = RAGPipeline(
                model_provider=model_provider,
                groq_api_key=groq_api_key
            )
            
            # Veritabanı kontrolü
            if os.path.exists("chroma_db"):
                rag.load_vectorstore()
                rag.create_qa_chain(k=4)
                st.session_state.vectorstore_loaded = True
                st.session_state.rag_pipeline = rag
                st.session_state.model_provider = model_provider
                st.success(f"✅ RAG sistemi başarıyla yüklendi! ({model_provider.upper()})")
                return True
            else:
                st.warning("⚠️ Vektör veritabanı bulunamadı. Lütfen önce verileri işleyin.")
                return False
                
    except Exception as e:
        st.error(f"❌ RAG sistemi yüklenirken hata: {str(e)}")
        return False


def process_data(model_provider: str, groq_api_key: str = None):
    """Veri işleme ve vektör veritabanı oluşturma"""
    try:
        with st.spinner("📊 Veriler işleniyor..."):
            # Data processor oluştur
            processor = DataProcessor(chunk_size=1000, chunk_overlap=200)
            
            # Veri dizinini kontrol et
            if not os.path.exists('data'):
                st.error("❌ 'data' klasörü bulunamadı!")
                return False
            
            # Verileri işle
            documents = processor.process_directory('data')
            
            if len(documents) == 0:
                st.error("❌ İşlenecek veri bulunamadı!")
                return False
            
            st.info(f"📄 {len(documents)} chunk oluşturuldu")
            
        with st.spinner("🔨 Vektör veritabanı oluşturuluyor..."):
            # RAG pipeline oluştur
            rag = RAGPipeline(
                model_provider=model_provider,
                groq_api_key=groq_api_key
            )
            
            # Vektör veritabanı oluştur
            rag.create_vectorstore(documents)
            
            # QA zinciri oluştur
            rag.create_qa_chain(k=4)
            
            st.session_state.rag_pipeline = rag
            st.session_state.vectorstore_loaded = True
            
            st.success(f"✅ Vektör veritabanı başarıyla oluşturuldu! ({len(documents)} chunk)")
            return True
            
    except Exception as e:
        st.error(f"❌ Veri işleme hatası: {str(e)}")
        return False


def display_chat_message(role: str, content: str):
    """Chat mesajını gösterir"""
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>👤 Sen:</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message bot-message">
            <strong>🎬 Film Gurusu:</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)


def main():
    """Ana uygulama fonksiyonu"""
    # Session state başlat
    initialize_session_state()
    
    # Başlık
    st.markdown("<h1>🎬 Film Gurusu</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>RAG Tabanlı Film Eleştiri Chatbot'u</p>", unsafe_allow_html=True)
    
    # Sidebar - Ayarlar
    with st.sidebar:
        st.header("⚙️ Ayarlar")
        
        # API Key'leri .env'den otomatik yükle
        load_dotenv()
        groq_api_key = os.getenv('GROQ_API_KEY')
        
        # Model Seçimi
        st.subheader("🤖 Model Seçimi")
        model_provider = st.selectbox(
            "LLM Provider",
            ["ollama", "groq"],
            index=0,  # Ollama varsayılan (lokal)
            help="Hangi AI modelini kullanmak istiyorsunuz?"
        )
        
        # Model bilgileri ve API key durumu
        if model_provider == "ollama":
            st.info("🏠 **Ollama - Phi-3 Mini (3.8B)**\n- Tamamen LOKAL\n- API key gerektirmez\n- Offline çalışır\n- CPU'da hızlı")
            st.success("✅ Ollama: Lokal (API key gerekmez)")
            keys_configured = True  # Ollama için API key gerekmez
            
        elif model_provider == "groq":
            st.info("⚡ **Groq - Llama 3.2 90B**\n- Çok hızlı\n- Ücretsiz kuota\n- Türkçe desteği mükemmel")
            if groq_api_key:
                st.success("✅ Groq API: Aktif")
                keys_configured = True
            else:
                st.warning("⚠️ Groq API key bulunamadı (.env dosyasına GROQ_API_KEY ekleyin)")
                st.info("🔗 API key almak için: https://console.groq.com/keys")
                keys_configured = False
        
        st.session_state.api_key_configured = keys_configured
        
        st.divider()
        
        # RAG sistemi yükleme
        st.header("🚀 Sistem Kontrolü")
        
        if keys_configured:
            # RAG sistemi yükleme butonu
            if not st.session_state.vectorstore_loaded:
                if st.button("🚀 RAG Sistemini Başlat"):
                    success = load_rag_pipeline(model_provider, groq_api_key)
                    if not success:
                        st.info("💡 Vektör veritabanı yoksa, önce 'Verileri İşle' butonuna tıklayın")
            else:
                current_model = st.session_state.model_provider.upper()
                st.success(f"✅ RAG sistemi aktif ({current_model})")
                
                # Model değişikliği kontrolü
                if st.session_state.model_provider != model_provider:
                    st.warning(f"⚠️ Model değişti! Yeniden başlatın.")
                    if st.button("🔄 Modeli Değiştir"):
                        st.session_state.vectorstore_loaded = False
                        st.rerun()
        else:
            st.warning("⚠️ Groq kullanmak için API key gerekli")
        
        st.divider()
        
        # Veri işleme bölümü
        st.header("📚 Veri Yönetimi")
        
        if keys_configured:
            if st.button("🔄 Verileri İşle"):
                if process_data(model_provider, groq_api_key):
                    st.rerun()
            
            st.caption("💡 Yeni veri eklediyseniz, bu butona tıklayarak veritabanını güncelleyin.")
        else:
            st.warning("⚠️ Groq kullanmak için API key gerekli")
        
        st.divider()
        
        # Sohbet temizleme
        st.header("💬 Sohbet")
        if st.button("🗑️ Sohbeti Temizle"):
            st.session_state.messages = []
            st.rerun()
        
        st.divider()
        
        # İstatistikler
        st.header("📊 İstatistikler")
        st.metric("Mesaj Sayısı", len(st.session_state.messages))
        
        if st.session_state.vectorstore_loaded:
            st.success("🟢 Veritabanı: Aktif")
        else:
            st.error("🔴 Veritabanı: Pasif")
        
        st.divider()
        
        # Hakkında
        st.header("ℹ️ Hakkında")
        st.markdown("""
        **Film Gurusu Chatbot**
        
        Bu chatbot, RAG (Retrieval-Augmented Generation) 
        teknolojisi kullanarak film eleştirileri üzerine 
        sorularınızı yanıtlar.
        
        **Teknolojiler:**
        - 🤖 Ollama (Phi-3 Mini) / Groq (Llama 3.2 90B)
        - 🔗 LangChain
        - 💾 ChromaDB (Vektör DB)
        - 🎨 Streamlit
        - 🧠 Custom Transformers (Lokal Embedding)
        
        ---
        *Akbank GenAI Bootcamp*  
        *Yeni Nesil Proje Kampı*
        """)
    
    # Ana içerik - Chat arayüzü
    if not st.session_state.api_key_configured:
        st.warning("⚠️ API Key gerekli!")
        st.info("📝 Groq kullanmak için `.env` dosyasına API key ekleyin:")
        st.code("""
# .env dosyası
GROQ_API_KEY=your_groq_api_key_here
        """, language="bash")
        st.info("🔗 Ücretsiz Groq API key almak için: https://console.groq.com/keys")
        st.divider()
        st.success("💡 **Veya Ollama kullanın** (API key gerekmez, tamamen lokal!)")
        st.info("Sol panelden 'ollama' seçeneğini seçin ve direkt başlayın.")
        
        # Örnek sorular
        st.subheader("💡 Hazır Olunca Sorabilecekleriniz:")
        example_questions = [
            "Christopher Nolan'ın hangi filmleri hakkında eleştiri var?",
            "En iyi puan alan filmler hangileri?",
            "Parasite filmi hakkında ne söyleniyor?",
            "Duygusal filmler önerir misin?",
            "Hangi filmler sosyal eleştiri içeriyor?"
        ]
        
        for question in example_questions:
            st.markdown(f"- {question}")
    
    elif not st.session_state.vectorstore_loaded:
        st.warning("⚠️ RAG sistemi henüz yüklenmedi. Lütfen sol panelden '🚀 RAG Sistemini Başlat' butonuna tıklayın.")
        st.info("💡 Eğer vektör veritabanı yoksa, önce '🔄 Verileri İşle' butonuna tıklayın.")
    
    else:
        # Chat geçmişini göster
        for message in st.session_state.messages:
            display_chat_message(message["role"], message["content"])
        
        # Kullanıcı girişi
        user_question = st.chat_input("Film hakkında bir şey sor... 🎬")
        
        if user_question:
            # Kullanıcı mesajını ekle
            st.session_state.messages.append({
                "role": "user",
                "content": user_question
            })
            
            # Kullanıcı mesajını göster
            display_chat_message("user", user_question)
            
            # Bot cevabını al
            with st.spinner("🤔 Düşünüyorum..."):
                try:
                    result = st.session_state.rag_pipeline.query(user_question)
                    bot_response = result['answer']
                    
                    # Bot mesajını ekle
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": bot_response
                    })
                    
                    # Bot mesajını göster
                    display_chat_message("assistant", bot_response)
                    
                    # Kaynak belgeleri göster (expander içinde)
                    if result['source_documents']:
                        with st.expander("📚 Kaynak Belgeler"):
                            for i, doc in enumerate(result['source_documents'], 1):
                                st.markdown(f"**Kaynak {i}:**")
                                st.text(doc.page_content[:300] + "...")
                                st.divider()
                    
                except Exception as e:
                    error_message = f"Üzgünüm, bir hata oluştu: {str(e)}"
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_message
                    })
                    display_chat_message("assistant", error_message)
            
            # Sayfayı yenile
            st.rerun()


if __name__ == "__main__":
    # .env dosyasını yükle
    load_dotenv()
    
    # Uygulamayı çalıştır
    main()

