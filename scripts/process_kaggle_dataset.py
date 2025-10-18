import os
import argparse
from dotenv import load_dotenv
from src.data_processor import DataProcessor
from src.rag_pipeline import RAGPipeline


def main():
    parser = argparse.ArgumentParser(description="Build FAISS index from Kaggle dataset directory")
    parser.add_argument("--data-dir", default="data", help="Dataset directory containing CSV/JSON/TXT files")
    parser.add_argument("--model", choices=["gemini", "ollama"], default="gemini", help="LLM provider to initialize")
    parser.add_argument("--k", type=int, default=2, help="Retriever top-k during chain creation")
    args = parser.parse_args()

    load_dotenv()

    processor = DataProcessor(chunk_size=1000, chunk_overlap=200)
    documents = processor.process_directory(args.data_dir)

    rag = RAGPipeline(model_provider=args.model)
    rag.create_vectorstore(documents)
    rag.create_qa_chain(k=args.k)
    print("Index build completed.")


if __name__ == "__main__":
    main()


