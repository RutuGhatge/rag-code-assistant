import os
from src.data_ingestion import load_pdfs
from src.embedding_store import get_or_create_vector_store
from src.rag_pipeline import create_qa_chain, ask_question
from src.stackoverflow_scraper import scrape_stackoverflow
from src.config import PDF_DIR, FAISS_INDEX, STACKOVERFLOW_DIR, MAX_RESULTS

print(">>")
topic = input("Enter the topic you want to search on Stack Overflow: ").strip()

# ✅ Load and chunk PDFs
print("Loading PDF documents...")
pdf_docs = load_pdfs(PDF_DIR)
print(f"✅ Loaded and split into {len(pdf_docs)} chunks.")

# ✅ Create FAISS vector store
vector_store = get_or_create_vector_store(pdf_docs)  # FIXED here

# ✅ Create QA Chain
qa_chain = create_qa_chain(vector_store)

# ✅ Fetch Stack Overflow Questions
stack_results = scrape_stackoverflow(topic, MAX_RESULTS, STACKOVERFLOW_DIR)

while True:
    query = input("\nEnter your question (or type 'exit' to quit): ").strip()
    if query.lower() in ["exit", "quit"]:
        break

    # Get PDF-based answer
    pdf_answer = ask_question(qa_chain, query)

    # Show combined output
    print("\n📘 Answer from PDFs:\n", pdf_answer)
    print("\n🔥 Top Stack Overflow Discussions:\n")
    for i, r in enumerate(stack_results[:10], 1):
        print(f"{i}. Q: {r.get('title')}\n   Link: {r.get('link')}\n")
