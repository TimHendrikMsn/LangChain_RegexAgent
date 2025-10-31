from src.settings import settings
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import shutil


def load_document(path): 
    """Load a text document from the given path to prepare RAG."""
    loader = TextLoader(path)
    document = loader.load()
    return document


def split_text(document):
    """Split document into overlapping text chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(document)

    return chunks

def save_to_chroma(chunks):
    """Save text chunks to a Chroma vector store."""
    if os.path.exists(settings.chroma_path):
        shutil.rmtree(settings.chroma_path)

    Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory=settings.chroma_path
    )