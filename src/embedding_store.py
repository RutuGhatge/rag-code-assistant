import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from src.config import FAISS_INDEX

def get_or_create_vector_store(documents):
    if os.path.exists(FAISS_INDEX):
        print("✅ Loading existing FAISS vector store...")
        return FAISS.load_local(FAISS_INDEX, HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"), allow_dangerous_deserialization=True)

    print("Creating FAISS vector store...")
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(documents, embedding_model)
    vector_store.save_local(FAISS_INDEX)
    print("✅ FAISS vector store saved!")
    return vector_store
