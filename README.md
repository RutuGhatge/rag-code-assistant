# RAG-Based Python Code Assistant

This project is a **Retrieval-Augmented Generation (RAG) system** that combines:
* **PDF documents** (Python books)
* **Stack Overflow questions**
* **FAISS vector search**
* **HuggingFace LLM** for answering user queries.

---

## **Features**
* ✔ Loads multiple Python PDF books.
* ✔ Scrapes top **Stack Overflow** questions for a given topic.
* ✔ Splits documents into chunks and stores embeddings in **FAISS**.
* ✔ Answers user queries using **retrieved content + LLM**.
* ✔ Configurable via `config.py`.

---

## **Project Structure**

RAG_CODE_ASSISTANT/
│
├── data/
│   ├── Python-books/       # PDF files
│   ├── stackoverflow/      # Saved Stack Overflow data
│   └── stackoverflow_cache/# Cached results
│
├── faiss_store/            # FAISS index
│
├── src/
│   ├── config.py           # Configuration settings
│   ├── data_ingestion.py   # Loads PDFs and text
│   ├── text_processing.py  # Chunking and cleaning
│   ├── embedding_store.py  # FAISS vector store creation
│   ├── retriever.py        # Retriever for RAG
│   ├── rag_pipeline.py     # LLM pipeline (HuggingFace)
│   └── init.py
│
├── main.py                 # Main script
├── requirements.txt        # Dependencies
└── README.md


---

## **Installation**

1.  Clone the repo:
    ```bash
    git clone <your-repo-link>
    cd RAG_CODE_ASSISTANT
    ```
2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    # For Linux/Mac:
    source venv/bin/activate
    # For Windows:
    venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

---

## **Usage**

1.  Place your Python PDF books in:
    ```
    data/Python-books/
    ```
2.  Run the script:
    ```bash
    python main.py
    ```
3.  Enter:
    * **Topic** (e.g., `python decorators`)
    * Your **question** (e.g., `Explain python decorators with examples`)

---

## **Configuration**

All configurable parameters are in `src/config.py`:

```python
PDF_DIR = "data/Python-books/"
STACKOVERFLOW_DIR = "data/stackoverflow/"
FAISS_INDEX = "faiss_store"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "facebook/bart-large"
SCRAPE_MODE = "api"  # options: "api" or "selenium"
MAX_RESULTS = 10
```
---
## Example Workflow
```
Loads PDFs → Converts to text → Chunks.

Creates FAISS index with sentence-transformer embeddings.

Scrapes top 10 Stack Overflow questions for your topic.

Retrieves relevant context from PDFs and SO questions.

Passes combined context + question to HuggingFace LLM.

Outputs the best answer.

```
---
## Dependencies
langchain
faiss-cpu
sentence-transformers
transformers
pypdf
beautifulsoup4
requests
langchain-community
selenium 
webdriver-manager 

