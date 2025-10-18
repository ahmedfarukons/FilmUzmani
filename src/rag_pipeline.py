"""
RAG Pipeline - Retrieval-Augmented Generation sistemi
"""
import os

# TensorFlow'u devre dışı bırak (sadece PyTorch kullan)
os.environ['USE_TF'] = 'NO'
os.environ['USE_TORCH'] = 'YES'

from typing import List, Optional
from dotenv import load_dotenv
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI


class RAGPipeline:
    """RAG pipeline sınıfı - FAISS vektör DB ve çeşitli LLM'ler kullanarak soru-cevap sistemi"""
    
    def __init__(
        self, 
        persist_directory: str = "faiss_db",
        model_provider: str = "ollama",
        api_key: Optional[str] = None
    ):
        """
        RAG Pipeline'ı başlatır
        
        Args:
            persist_directory: FAISS veritabanı dizini
            model_provider: LLM sağlayıcısı ("ollama" veya "gemini")
            api_key: API anahtarı (Gemini için gerekli, .env'den okunabilir)
        """
        # .env dosyasını yükle
        load_dotenv()
        
        self.persist_directory = persist_directory
        self.model_provider = model_provider.lower()
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.embeddings = None
        self.vectorstore = None
        self.llm = None
        self.qa_chain = None
        
        # Embedding modelini başlat
        self._initialize_embeddings()
        
        # LLM'i başlat
        self._initialize_llm()
    
    def _initialize_embeddings(self):
        """Embedding modelini başlatır - Custom Transformers Embeddings (sentence-transformers olmadan)"""
        try:
            # Direkt transformers kullan, sentence-transformers'a gerek yok
            from transformers import AutoTokenizer, AutoModel
            import torch
            from langchain.embeddings.base import Embeddings
            from typing import List
            
            print("📥 Embedding modeli yükleniyor (lokal, transformers kullanarak)...")
            
            # Custom embedding class
            class CustomTransformerEmbeddings(Embeddings):
                def __init__(self):
                    self.tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
                    self.model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
                    self.model.eval()
                
                def embed_documents(self, texts: List[str]) -> List[List[float]]:
                    embeddings = []
                    for text in texts:
                        encoded = self.tokenizer(text, padding=True, truncation=True, return_tensors='pt', max_length=512)
                        with torch.no_grad():
                            output = self.model(**encoded)
                        # Mean pooling
                        embedding = output.last_hidden_state.mean(dim=1).squeeze().tolist()
                        embeddings.append(embedding)
                    return embeddings
                
                def embed_query(self, text: str) -> List[float]:
                    encoded = self.tokenizer(text, padding=True, truncation=True, return_tensors='pt', max_length=512)
                    with torch.no_grad():
                        output = self.model(**encoded)
                    embedding = output.last_hidden_state.mean(dim=1).squeeze().tolist()
                    return embedding
            
            self.embeddings = CustomTransformerEmbeddings()
            print("✅ Embedding modeli başlatıldı (Custom Transformers - LOKAL)")
            
        except Exception as e:
            print(f"❌ Embedding hatası: {str(e)}")
            import traceback
            traceback.print_exc()
            raise Exception(f"Lokal embedding modeli başlatılamadı: {str(e)}")
    
    def _initialize_llm(self):
        """LLM modelini başlatır"""
        try:
            if self.model_provider == "ollama":
                # Ollama - Tamamen lokal, API key gerektirmez
                ollama_base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
                ollama_model = os.getenv('OLLAMA_MODEL', 'phi3:mini')
                temperature = float(os.getenv('OLLAMA_TEMPERATURE', '0.5'))
                num_predict = int(os.getenv('OLLAMA_NUM_PREDICT', '512'))
                self.llm = ChatOllama(
                    model=ollama_model,
                    temperature=temperature,
                    base_url=ollama_base_url,
                    num_predict=num_predict
                )
                print(f"✓ Ollama modeli başlatıldı: {ollama_model} ({ollama_base_url})")
            
            elif self.model_provider == "gemini":
                if not self.api_key:
                    raise ValueError("Gemini API anahtarı bulunamadı. .env dosyasına GEMINI_API_KEY ekleyin.")
                
                gemini_model = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
                temperature = float(os.getenv('GEMINI_TEMPERATURE', '0.7'))
                self.llm = ChatGoogleGenerativeAI(
                    model=gemini_model,
                    google_api_key=self.api_key,
                    temperature=temperature,
                    convert_system_message_to_human=True
                )
                print(f"✓ Google Gemini modeli başlatıldı: {gemini_model} 🚀")
            
            else:
                raise ValueError(f"Desteklenmeyen model: {self.model_provider}. Sadece 'ollama' veya 'gemini' destekleniyor.")
                
        except Exception as e:
            raise Exception(f"LLM başlatılamadı: {str(e)}")
    
    def create_vectorstore(self, documents: List[Document]):
        """
        Belgelerden vektör veritabanı oluşturur
        
        Args:
            documents: Document nesnelerinin listesi
        """
        try:
            print(f"\n📊 {len(documents)} belge vektör veritabanına ekleniyor...")
            
            # FAISS vektör DB oluştur
            self.vectorstore = FAISS.from_documents(
                documents=documents,
                embedding=self.embeddings
            )
            
            # FAISS'i kaydet
            self.vectorstore.save_local(self.persist_directory)
            print(f"✓ Vektör veritabanı oluşturuldu ve kaydedildi: {self.persist_directory}")
            
        except Exception as e:
            raise Exception(f"Vektör veritabanı oluşturulamadı: {str(e)}")
    
    def load_vectorstore(self):
        """Mevcut vektör veritabanını yükler"""
        try:
            if not os.path.exists(self.persist_directory):
                raise FileNotFoundError(f"Vektör veritabanı bulunamadı: {self.persist_directory}")
            
            # FAISS'i yükle
            self.vectorstore = FAISS.load_local(
                self.persist_directory,
                embeddings=self.embeddings,
                allow_dangerous_deserialization=True  # Local dosya güvenli
            )
            print("✓ Vektör veritabanı yüklendi")
            
        except Exception as e:
            raise Exception(f"Vektör veritabanı yüklenemedi: {str(e)}")
    
    def create_qa_chain(self, k: int = 4):
        """
        Soru-cevap zinciri oluşturur
        
        Args:
            k: Her sorgu için alınacak benzer belge sayısı
        """
        if self.vectorstore is None:
            raise ValueError("Önce vektör veritabanı oluşturulmalı veya yüklenmelidir")
        
        try:
            # Retriever oluştur
            retriever = self.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": k}
            )
            
            # QA zinciri oluştur
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True,
                verbose=False
            )
            
            print(f"✓ QA zinciri oluşturuldu (k={k}) - HIZLI MOD AKTİF")
            
        except Exception as e:
            raise Exception(f"QA zinciri oluşturulamadı: {str(e)}")
    
    def query(self, question: str) -> dict:
        """
        Kullanıcı sorusuna cevap üretir
        
        Args:
            question: Kullanıcının sorusu
            
        Returns:
            Cevap ve kaynak belgeler içeren dict
        """
        if self.qa_chain is None:
            raise ValueError("Önce QA zinciri oluşturulmalıdır")
        
        try:
            # Prompt'u Türkçe için optimize et
            enhanced_question = f"""
Sen bir film uzmanı asistanısın. Sana verilen film eleştirileri bilgi tabanını kullanarak 
kullanıcının sorusuna detaylı, bilgilendirici ve dostça bir şekilde cevap ver.

Kullanıcı Sorusu: {question}

Lütfen cevabını Türkçe olarak ver ve mümkünse bilgi tabanındaki spesifik film örnekleriyle destekle.
"""
            
            # Sorguyu çalıştır (invoke kullan, __call__ deprecated)
            result = self.qa_chain.invoke({"query": enhanced_question})
            
            return {
                'answer': result['result'],
                'source_documents': result['source_documents'],
                'question': question
            }
            
        except Exception as e:
            return {
                'answer': f"Üzgünüm, bir hata oluştu: {str(e)}",
                'source_documents': [],
                'question': question
            }
    
    def get_similar_documents(self, query: str, k: int = 3) -> List[Document]:
        """
        Sorguya en benzer belgeleri döndürür
        
        Args:
            query: Arama sorgusu
            k: Döndürülecek belge sayısı
            
        Returns:
            Benzer belgelerin listesi
        """
        if self.vectorstore is None:
            raise ValueError("Önce vektör veritabanı oluşturulmalı veya yüklenmelidir")
        
        try:
            docs = self.vectorstore.similarity_search(query, k=k)
            return docs
        except Exception as e:
            raise Exception(f"Benzer belgeler alınamadı: {str(e)}")


def main():
    """Test fonksiyonu"""
    try:
        # RAG Pipeline oluştur
        rag = RAGPipeline()
        
        # Test sorgusu
        print("\n🧪 Test Sorgusu")
        print("-" * 50)
        
        # Eğer veritabanı varsa yükle, yoksa uyarı ver
        if os.path.exists("faiss_db"):
            rag.load_vectorstore()
            rag.create_qa_chain()
            
            test_question = "Christopher Nolan'ın en iyi filmleri hangileri?"
            print(f"\nSoru: {test_question}")
            
            result = rag.query(test_question)
            print(f"\nCevap:\n{result['answer']}")
            
            print(f"\n📚 Kullanılan kaynak sayısı: {len(result['source_documents'])}")
        else:
            print("⚠️  Vektör veritabanı bulunamadı. Önce verileri işleyin.")
            
    except Exception as e:
        print(f"❌ Hata: {str(e)}")


if __name__ == "__main__":
    main()

