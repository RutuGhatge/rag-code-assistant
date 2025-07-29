import os
import pprint
from src.data_ingestion import load_pdfs
from src.embedding_store import get_or_create_vector_store
from src.rag_pipeline import create_qa_chain, ask_question
from src.stackoverflow_scraper import scrape_stackoverflow
from src.config import PDF_DIR, STACKOVERFLOW_DIR, MAX_RESULTS


def get_answers_for_query(topic: str, query: str):
    """
    Returns a list with two dictionaries: one for the PDF answer, one for Stack Overflow results.
    Args:
        topic (str): Topic to focus Stack Overflow search.
        query (str): The user's question.

    Returns:
        list: [
            {'source': 'pdf', 'answer': str},
            {'source': 'stackoverflow', 'results': list of {'title': str, 'content': str}}
        ]
    """
    try:
        # Setup
        pdf_docs = load_pdfs(PDF_DIR)
        vector_store = get_or_create_vector_store(pdf_docs)
        qa_chain = create_qa_chain(vector_store)

        # PDF-based answer
        pdf_answer = ask_question(qa_chain, query).strip()

        # Stack Overflow results
        stack_results = scrape_stackoverflow(f"{topic} {query}", MAX_RESULTS, STACKOVERFLOW_DIR)

        return [
            {"source": "pdf", "answer": pdf_answer},
            {"source": "stackoverflow", "results": stack_results or []}
        ]

    except Exception as e:
        return [
            {"source": "pdf", "answer": ""},
            {"source": "stackoverflow", "results": [], "error": str(e)}
        ]


def run_interactive_session():
    """
    Sets up the engine and runs the interactive session in a better structured topic-question workflow.
    """
    # --- Get Topic First ---
    topic = input("Enter the topic for Stack Overflow discussions: ").strip()

    # --- One-Time Setup ---
    print("\nInitializing the Code Assistant...")
    pdf_docs = load_pdfs(PDF_DIR)
    vector_store = get_or_create_vector_store(pdf_docs)
    qa_chain = create_qa_chain(vector_store)

    print("\n✅ Assistant is ready. Ask your specific question!")

    while True:
        try:
            query = input("\nEnter your question (or type 'exit' to quit): ").strip()
            if query.lower() in ["exit", "quit"]:
                break
            if not query:
                continue

            # --- Local PDF Search ---
            pdf_answer = ask_question(qa_chain, query)

            # --- Stack Overflow Search (filtered by topic + question) ---
            print(f"\n🔍 Searching Stack Overflow for: '{query}' under topic '{topic}'...")
            stack_results = scrape_stackoverflow(f"{topic} {query}", MAX_RESULTS, STACKOVERFLOW_DIR)

            # --- Display Answers ---
            print("\n" + "="*50)
            print("📘 Answer from your PDFs:")
            print("="*50)
            print(pdf_answer if pdf_answer.strip() else "No relevant information found in the provided PDF documents.")

            print("\n" + "="*50)
            print("🔥 Top Related Discussions from Stack Overflow:")
            print("="*50)

            if not stack_results:
                print("No relevant discussions found on Stack Overflow.")
            else:
                for i, result in enumerate(stack_results, 1):
                    print(f"\n{i}. Question: {result.get('title', 'No Title')}")
                    print("----------------------------------------")
                    print(result.get('content', 'No content scraped.'))

        except Exception as e:
            print(f"\nAn error occurred: {e}")


if __name__ == "__main__":
    run_interactive_session()
