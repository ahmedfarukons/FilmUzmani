import os
import sys
from dotenv import load_dotenv

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.rag_pipeline import RAGPipeline


def main():
    load_dotenv()
    model = os.getenv("SMOKE_MODEL", "gemini")
    question = os.getenv("SMOKE_QUESTION", "Christopher Nolan'ın en iyi filmleri hangileri?")

    rag = RAGPipeline(model_provider=model)
    rag.load_vectorstore()
    rag.create_qa_chain(k=2)
    result = rag.query(question)
    print("Answer:\n", result["answer"])


if __name__ == "__main__":
    main()


