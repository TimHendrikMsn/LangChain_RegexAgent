from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from src.settings import settings
import sys


def load_database(path):
    """
    Load a Chroma database from the given path using OpenAI embeddings.
    """
    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory=path, embedding_function=embedding_function)
    return db

def most_relevant_k_chunks(query, db, k=3):
    """
    Return the top-k most relevant text chunks for a query.
    """
    results = db.similarity_search_with_relevance_scores(query, k)
    if len(results) == 0 or results[0][1] < 0.7:
        return "Unable to find matching results."
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    return context_text

if __name__ == "__main__":
    db = load_database(path=settings.chroma_path)
    text = most_relevant_k_chunks(sys.argv[1], db, 3)
    print(text)
