from transformers import pipeline
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFacePipeline
from src.config import LLM_MODEL

def create_qa_chain(vector_store):
    """
    Creates the RAG chain using the 'map_reduce' method.
    """
    print("✅ Loading LLM...")

    llm_pipeline = pipeline(
        "text2text-generation",
        model=LLM_MODEL,
        max_new_tokens=512,
        device=0  # Use -1 for CPU, 0 for GPU
    )
    llm = HuggingFacePipeline(pipeline=llm_pipeline)

    # Prompt for processing each individual document chunk
    question_prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""You are an expert assistant. Use the given context to answer the question clearly.
- If the context is incomplete or irrelevant, answer based on your own general knowledge.

Context:
{context}

Question: {question}

Answer:
"""
    )

    # Prompt for combining the answers from all chunks
    combine_prompt = PromptTemplate(
        input_variables=["summaries", "question"],
        template="""You are an expert summarizer. Combine the following partial answers into a single, clear, and complete final response.

Partial Answers:
{summaries}

Question: {question}

Final Answer:
"""
    )

    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # Build the 'map_reduce' chain
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="map_reduce",
        chain_type_kwargs={
            "question_prompt": question_prompt,
            "combine_prompt": combine_prompt
        }
    )

def ask_question(qa_chain, query: str) -> str:
    """
    Queries the QA chain and returns the answer.
    """
    print(f"\n🔍 Querying the knowledge base for: '{query}'")
    result = qa_chain.invoke({"query": query})
    return result.get("result", "No answer could be generated.")