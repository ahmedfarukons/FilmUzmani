# -*- coding: utf-8 -*-
"""
Veri İşleme Modülü - Film eleştirilerini yükler ve chunking yapar
"""
import os
import sys
import io
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

# Windows için UTF-8 encoding ayarla
if sys.platform == 'win32':
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'buffer'):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


class DataProcessor:
    """Film eleştirilerini işlemek için sınıf"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        DataProcessor sınıfını başlatır
        
        Args:
            chunk_size: Her chunk'ın maksimum karakter sayısı
            chunk_overlap: Chunk'lar arasındaki örtüşme miktarı
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""],
            length_function=len
        )
    
    def load_text_file(self, file_path: str) -> str:
        """
        Metin dosyasını yükler
        
        Args:
            file_path: Dosya yolu
            
        Returns:
            Dosyanın içeriği
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            raise FileNotFoundError(f"Dosya bulunamadı: {file_path}")
        except Exception as e:
            raise Exception(f"Dosya okuma hatası: {str(e)}")
    
    def split_into_chunks(self, text: str, metadata: dict = None) -> List[Document]:
        """
        Metni küçük parçalara böler (chunking)
        
        Args:
            text: Bölünecek metin
            metadata: Chunk'lara eklenecek metadata
            
        Returns:
            Document nesnelerinin listesi
        """
        if metadata is None:
            metadata = {}
        
        # Metni parçalara böl
        chunks = self.text_splitter.split_text(text)
        
        # Her chunk için Document nesnesi oluştur
        documents = []
        for i, chunk in enumerate(chunks):
            doc_metadata = metadata.copy()
            doc_metadata['chunk_id'] = i
            doc_metadata['chunk_size'] = len(chunk)
            
            documents.append(Document(
                page_content=chunk,
                metadata=doc_metadata
            ))
        
        return documents
    
    def process_review_file(self, file_path: str) -> List[Document]:
        """
        Film eleştiri dosyasını işler ve chunk'lara böler
        
        Args:
            file_path: Eleştiri dosyasının yolu
            
        Returns:
            Document nesnelerinin listesi
        """
        # Dosyayı yükle
        content = self.load_text_file(file_path)
        
        # Metadata oluştur
        metadata = {
            'source': file_path,
            'type': 'film_review'
        }
        
        # Chunk'lara böl
        documents = self.split_into_chunks(content, metadata)
        
        print(f"✓ {len(documents)} chunk oluşturuldu: {file_path}")
        return documents
    
    def process_directory(self, directory_path: str) -> List[Document]:
        """
        Bir dizindeki tüm metin dosyalarını işler
        
        Args:
            directory_path: Dizin yolu
            
        Returns:
            Tüm dosyalardan oluşturulan Document'ların listesi
        """
        all_documents = []
        
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"Dizin bulunamadı: {directory_path}")
        
        # Dizindeki tüm .txt dosyalarını işle
        for filename in os.listdir(directory_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(directory_path, filename)
                documents = self.process_review_file(file_path)
                all_documents.extend(documents)
        
        print(f"\n✓ Toplam {len(all_documents)} chunk oluşturuldu")
        return all_documents


def main():
    """Test fonksiyonu"""
    processor = DataProcessor(chunk_size=1000, chunk_overlap=200)
    
    # Örnek kullanım
    try:
        documents = processor.process_directory('data')
        print(f"\nİşlenen toplam chunk sayısı: {len(documents)}")
        
        # İlk chunk'ı göster
        if documents:
            print(f"\nİlk chunk örneği:")
            print(f"İçerik uzunluğu: {len(documents[0].page_content)} karakter")
            print(f"Metadata: {documents[0].metadata}")
            print(f"\nİçerik önizleme:\n{documents[0].page_content[:200]}...")
            
    except Exception as e:
        print(f"Hata: {str(e)}")


if __name__ == "__main__":
    main()

