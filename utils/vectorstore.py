from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from utils.embeddings import get_embedding_model
  # <-- Bunu ekliyoruz

def create_vectorstore(chunks: list, persist_directory: str = 'db') -> Chroma:
    embeddings = get_embedding_model()
    docs = [Document(page_content=chunk, metadata={}) for chunk in chunks]
    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    vectordb.persist()
    return vectordb

def load_vectorstore(persist_directory: str = 'db') -> Chroma:
    embeddings = get_embedding_model()
    return Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
