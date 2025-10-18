import os
from dotenv import load_dotenv
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


