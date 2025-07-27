from transformers import pipeline # type: ignore
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFacePipeline

def create_qa_chain(vector_store):
    print("✅ Loading LLM...")

    # ✅ Load HuggingFace model
    llm_pipeline = pipeline(
        "text2text-generation",
        model="google/flan-t5-large",  # Better model than base
        max_new_tokens=512,  # Output token limit
        device=-1  # -1 for CPU, 0 for GPU
    )

    llm = HuggingFacePipeline(pipeline=llm_pipeline)

    # ✅ Custom prompt to avoid repetition and improve clarity
    custom_prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are an expert assistant. Use the given context to answer the question clearly and concisely.
- Explain in simple terms.
- Include examples if possible.
- Avoid repetition.
- If the context is incomplete, answer based on general knowledge.

Context:
{context}

Question: {question}

Answer:
"""
    )

    # ✅ Use FAISS retriever with top 3 results for better relevance
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # ✅ Use map_reduce for summarizing multiple chunks
    return RetrievalQA.from_chain_type(
        llm,
        retriever=retriever,
        chain_type="map_reduce",
        chain_type_kwargs={"prompt": custom_prompt}
    )

def ask_question(qa_chain, query):
    print(f"\n🔍 Query: {query}")
    result = qa_chain.invoke({"query": query})
    return result.get("result", "No answer found.")
