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
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama


class RAGPipeline:
    """RAG pipeline sınıfı - ChromaDB ve çeşitli LLM'ler kullanarak soru-cevap sistemi"""
    
    def __init__(
        self, 
        persist_directory: str = "chroma_db",
        model_provider: str = "ollama",
        groq_api_key: Optional[str] = None
    ):
        """
        RAG Pipeline'ı başlatır
        
        Args:
            persist_directory: ChromaDB veritabanı dizini
            model_provider: LLM sağlayıcısı ("ollama" veya "groq")
            groq_api_key: Groq API anahtarı (Groq kullanılacaksa)
        """
        # API anahtarlarını yükle
        if groq_api_key is None:
            load_dotenv()
            groq_api_key = os.getenv('GROQ_API_KEY')
        
        self.groq_api_key = groq_api_key
        self.persist_directory = persist_directory
        self.model_provider = model_provider.lower()
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
                self.llm = ChatOllama(
                    model="phi3:mini",  # Phi-3 Mini 3.8B
                    temperature=0.7,
                    base_url="http://localhost:11434"  # Ollama varsayılan port
                )
                print("✓ Ollama - Phi-3 Mini modeli başlatıldı (LOKAL)")
                
            elif self.model_provider == "groq":
                if not self.groq_api_key:
                    raise ValueError("Groq API anahtarı bulunamadı. Groq kullanmak için API key gerekli.")
                
                self.llm = ChatGroq(
                    model="llama-3.2-90b-text-preview",  # En güçlü model
                    groq_api_key=self.groq_api_key,
                    temperature=0.7,
                    max_tokens=2048
                )
                print("✓ Groq - Llama 3.2 90B modeli başlatıldı")
            else:
                raise ValueError(f"Desteklenmeyen model sağlayıcısı: {self.model_provider}. Sadece 'ollama' veya 'groq' destekleniyor.")
                
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
            
            self.vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
            
            # Veritabanını kaydet
            self.vectorstore.persist()
            print(f"✓ Vektör veritabanı oluşturuldu ve kaydedildi: {self.persist_directory}")
            
        except Exception as e:
            raise Exception(f"Vektör veritabanı oluşturulamadı: {str(e)}")
    
    def load_vectorstore(self):
        """Mevcut vektör veritabanını yükler"""
        try:
            if not os.path.exists(self.persist_directory):
                raise FileNotFoundError(f"Vektör veritabanı bulunamadı: {self.persist_directory}")
            
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
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
            
            print(f"✓ QA zinciri oluşturuldu (k={k})")
            
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
            
            # Sorguyu çalıştır
            result = self.qa_chain({"query": enhanced_question})
            
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
        if os.path.exists("chroma_db"):
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

