"""
Film Gurusu Chatbot - Streamlit Web Arayüzü
Akbank GenAI Bootcamp Projesi
"""
import os
import io
from contextlib import redirect_stdout, redirect_stderr
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
    
    if 'system_ready' not in st.session_state:
        st.session_state.system_ready = False
    
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = "ollama"  # Varsayılan Ollama (lokal)


def auto_initialize_system():
    """Sistem açılışında otomatik olarak RAG'i yükle"""
    if os.path.exists("faiss_db") and not st.session_state.vectorstore_loaded:
        try:
            # Seçili modelle RAG başlat
            rag = RAGPipeline(model_provider=st.session_state.selected_model)
            rag.load_vectorstore()
            rag.create_qa_chain(k=2)  # Daha hızlı için 2
            st.session_state.rag_pipeline = rag
            st.session_state.vectorstore_loaded = True
            st.session_state.system_ready = True
            return True
        except Exception as e:
            # Fallback: Gemini başarısızsa Ollama ile deneyelim
            try:
                rag = RAGPipeline(model_provider="ollama")
                rag.load_vectorstore()
                rag.create_qa_chain(k=2)
                st.session_state.rag_pipeline = rag
                st.session_state.vectorstore_loaded = True
                st.session_state.system_ready = True
                st.session_state.selected_model = "ollama"
                return True
            except Exception:
                st.session_state.system_ready = False
                return False
    elif not os.path.exists("faiss_db"):
        st.session_state.system_ready = False
        return False
    return st.session_state.vectorstore_loaded


def process_data():
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
            # Streamlit stdout/stderr kapalı olabilir; güvenli yönlendirme kullan
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                documents = processor.process_directory('data')
            
            if len(documents) == 0:
                st.error("❌ İşlenecek veri bulunamadı!")
                return False
            
            st.info(f"📄 {len(documents)} chunk oluşturuldu")
            
        with st.spinner("🔨 Vektör veritabanı oluşturuluyor..."):
            # RAG pipeline oluştur (seçili model ile)
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                rag = RAGPipeline(model_provider=st.session_state.selected_model)
            
            # Vektör veritabanı oluştur
            # Olası print'leri güvenli şekilde yönlendir
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                rag.create_vectorstore(documents)
            
            # QA zinciri oluştur (k=2 daha hızlı)
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                rag.create_qa_chain(k=2)
            
            st.session_state.rag_pipeline = rag
            st.session_state.vectorstore_loaded = True
            st.session_state.system_ready = True
            
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
    
    # Otomatik sistem başlatma
    auto_initialize_system()
    
    # Başlık
    st.markdown("<h1>🎬 Film Gurusu</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>RAG Tabanlı Film Eleştiri Chatbot'u - Tamamen Lokal</p>", unsafe_allow_html=True)
    
    # Sidebar - Kontrol Paneli
    with st.sidebar:
        st.header("🤖 Model Seçimi")
        
        # Model seçici
        new_model = st.radio(
            "LLM Modeli:",
            options=["gemini", "ollama"],
            format_func=lambda x: "🚀 Gemini 1.5 Flash (Hızlı)" if x == "gemini" else "🏠 Ollama Phi-3 (Lokal)",
            index=0 if st.session_state.selected_model == "gemini" else 1,
            help="Gemini: Hızlı ve güçlü (API key gerekli)\nOllama: Tamamen lokal (yavaş olabilir)"
        )
        
        # Model değiştiyse sistemi resetle
        if new_model != st.session_state.selected_model:
            st.session_state.selected_model = new_model
            st.session_state.vectorstore_loaded = False
            st.session_state.system_ready = False
            st.session_state.rag_pipeline = None
            st.info("🔄 Model değişti, sistem yeniden başlatılıyor...")
            st.rerun()
        
        # API key kontrolü (sadece Gemini için)
        if st.session_state.selected_model == "gemini":
            load_dotenv()
            gemini_key = os.getenv('GEMINI_API_KEY')
            if not gemini_key:
                st.error("⚠️ GEMINI_API_KEY bulunamadı!")
                st.info("📝 .env dosyasına ekleyin:\n```\nGEMINI_API_KEY=your_key_here\n```")
            else:
                st.success("✅ API Key: " + gemini_key[:8] + "...")
        
        st.divider()
        
        st.header("📊 Sistem Durumu")
        
        # Sistem durumu göstergesi
        if st.session_state.system_ready and st.session_state.vectorstore_loaded:
            st.success("🟢 **Sistem Hazır**")
            model_name = "Gemini 1.5 Flash" if st.session_state.selected_model == "gemini" else "Ollama Phi-3 Mini"
            st.info(f"🤖 **Model:** {model_name}\n💾 **Vektör DB:** FAISS (Aktif)")
        elif os.path.exists("faiss_db") and not st.session_state.vectorstore_loaded:
            st.warning("🟡 **Yükleniyor...**")
            if st.button("🔄 Yeniden Yükle"):
                st.session_state.vectorstore_loaded = False
                st.rerun()
        else:
            st.error("🔴 **Veritabanı Yok**")
            st.info("💡 Önce verileri işleyin")
        
        st.divider()
        
        # Veri İşleme
        st.header("📚 Veri Yönetimi")
        if st.button("🔄 Verileri İşle / Güncelle"):
            if process_data():
                st.rerun()
        
        st.caption("💡 Yeni veri eklediyseniz bu butona tıklayın")
        
        st.divider()
        
        # Sohbet Kontrolü
        st.header("💬 Sohbet")
        if st.button("🗑️ Sohbeti Temizle"):
            st.session_state.messages = []
            st.rerun()
        
        st.metric("Mesaj Sayısı", len(st.session_state.messages))
        
        st.divider()
        
        # Hakkında
        st.header("ℹ️ Hakkında")
        st.markdown("""
        **Film Gurusu Chatbot**
        
        RAG teknolojisiyle film eleştirileri 
        üzerine sorularınızı yanıtlar.
        
        **Teknolojiler:**
        - 🤖 Gemini / Ollama
        - 🔗 LangChain
        - 💾 FAISS Vektör DB
        - 🎨 Streamlit
        - 🧠 Transformers Embeddings
        
        **Hybrid Model Desteği!**
        
        ---
        *Akbank GenAI Bootcamp*
        """)
    
    # Ana içerik - Chat arayüzü
    if not st.session_state.vectorstore_loaded:
        st.warning("⚠️ Vektör veritabanı bulunamadı!")
        st.info("💡 Sol panelden '🔄 Verileri İşle / Güncelle' butonuna tıklayın.")
        
        # Örnek sorular göster
        st.subheader("💡 Hazır Olunca Sorabilecekleriniz:")
        example_questions = [
            "Christopher Nolan'ın hangi filmleri hakkında eleştiri var?",
            "En iyi puan alan filmler hangileri?",
            "Duygusal filmler önerir misin?",
            "Hangi filmler sosyal eleştiri içeriyor?",
            "Aksiyon filmleri öner"
        ]
        
        for question in example_questions:
            st.markdown(f"- {question}")
    
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
    # Uygulamayı çalıştır
    main()

