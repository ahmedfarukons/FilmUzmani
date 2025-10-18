# -*- coding: utf-8 -*-
"""
Veri İşleme Modülü - Film eleştirilerini yükler ve chunking yapar
"""
import os
import sys
import io
from typing import List
import json
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

# Not: Streamlit ortamında stdout/stderr'i yeniden sarmalamak I/O hatalarına yol açabilir.
# Bu nedenle Windows'ta da varsayılan akışları olduğu gibi bırakıyoruz.


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
        Bir dizindeki .txt, .csv, .json dosyalarını işler
        
        Args:
            directory_path: Dizin yolu
            
        Returns:
            Tüm dosyalardan oluşturulan Document'ların listesi
        """
        all_documents = []
        
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"Dizin bulunamadı: {directory_path}")
        
        # Dizindeki desteklenen dosyaları işle
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            lower = filename.lower()
            try:
                if lower.endswith('.txt'):
                    documents = self.process_review_file(file_path)
                    all_documents.extend(documents)
                elif lower.endswith('.csv'):
                    documents = self.process_csv_file(file_path)
                    all_documents.extend(documents)
                elif lower.endswith('.json') or lower.endswith('.jsonl'):
                    documents = self.process_json_file(file_path)
                    all_documents.extend(documents)
            except Exception as e:
                print(f"Dosya atlandı (hata): {filename} -> {str(e)}")
        
        print(f"\n✓ Toplam {len(all_documents)} chunk oluşturuldu")
        return all_documents

    # --- Kaggle/donanımlı yükleyiciler ---

    def _infer_text_columns(self, df: pd.DataFrame) -> List[str]:
        """
        Kaggle veri setlerinde sık görülen metin sütunlarını sezgisel olarak belirler.
        """
        candidate_names = [
            'review', 'review_text', 'text', 'content', 'comment', 'plot', 'summary',
            'overview', 'description', 'body'
        ]
        found = [col for col in df.columns if col.lower() in candidate_names]
        if found:
            return found
        # Tipi string olan uzun metin sütunlarını sezgisel seç
        text_like = []
        for col in df.columns:
            series = df[col]
            if series.dtype == object:
                # Ortalama uzunluk kontrolü
                try:
                    sample = series.dropna().astype(str).head(50).tolist()
                    avg_len = sum(len(s) for s in sample) / max(1, len(sample))
                    if avg_len > 50:
                        text_like.append(col)
                except Exception:
                    continue
        return text_like[:2] if text_like else []

    def _compose_record_text(self, row: dict, text_cols: List[str], title_cols: List[str]) -> str:
        parts = []
        title = None
        for tcol in title_cols:
            if tcol in row and isinstance(row[tcol], str) and row[tcol].strip():
                title = row[tcol].strip()
                break
        if title:
            parts.append(f"Başlık: {title}")
        for col in text_cols:
            if col in row and isinstance(row[col], str) and row[col].strip():
                parts.append(row[col].strip())
        if not parts:
            # Fallback: tüm string alanları birleştir
            parts = [str(v) for v in row.values() if isinstance(v, str) and v.strip()]
        return "\n\n".join(parts)

    def process_csv_file(self, file_path: str) -> List[Document]:
        """
        CSV dosyasını yükler ve metin alanlarını chunk'lara böler.
        """
        df = pd.read_csv(file_path)
        # Başlık benzeri sütunlar
        title_candidates = ['title', 'movie', 'movie_title', 'film', 'name']
        title_cols = [c for c in df.columns if c.lower() in title_candidates]
        text_cols = self._infer_text_columns(df)

        documents: List[Document] = []
        for idx, row in df.iterrows():
            text = self._compose_record_text(row, text_cols, title_cols)
            if not text:
                continue
            meta = {
                'source': file_path,
                'type': 'csv_record',
                'row_index': int(idx)
            }
            # Satırı chunk'la
            documents.extend(self.split_into_chunks(text, meta))
        print(f"✓ CSV işlendi: {file_path} -> {len(documents)} chunk")
        return documents

    def process_json_file(self, file_path: str) -> List[Document]:
        """
        JSON veya JSONL dosyasını yükler ve metin alanlarını chunk'lara böler.
        """
        records: List[dict] = []
        with open(file_path, 'r', encoding='utf-8') as f:
            first = f.read(1)
            f.seek(0)
            if first == '[':
                # JSON array
                records = json.load(f)
            else:
                # JSONL
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue

        if not records:
            return []

        df = pd.DataFrame(records)
        title_candidates = ['title', 'movie', 'movie_title', 'film', 'name']
        title_cols = [c for c in df.columns if c.lower() in title_candidates]
        text_cols = self._infer_text_columns(df)

        documents: List[Document] = []
        for idx, row in df.iterrows():
            row_dict = row.to_dict()
            text = self._compose_record_text(row_dict, text_cols, title_cols)
            if not text:
                continue
            meta = {
                'source': file_path,
                'type': 'json_record',
                'row_index': int(idx)
            }
            documents.extend(self.split_into_chunks(text, meta))
        print(f"✓ JSON işlendi: {file_path} -> {len(documents)} chunk")
        return documents


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

