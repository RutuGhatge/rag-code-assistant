import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_pdfs(pdf_dir):
    documents = []
    for file_name in os.listdir(pdf_dir):
        if file_name.endswith(".pdf"):
            path = os.path.join(pdf_dir, file_name)
            print(f"📄 Loading PDF: {file_name}")
            loader = PyPDFLoader(path)
            documents.extend(loader.load())

    # ✅ Chunk the documents for better retrieval
    print("🔍 Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunked_docs = text_splitter.split_documents(documents)
    print(f"✅ Total chunks created: {len(chunked_docs)}")

    return chunked_docs
