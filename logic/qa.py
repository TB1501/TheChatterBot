from flask import jsonify, request
from langchain_chroma import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
import os

#db for processed data
folder_path = "db"

#embedding model
embedding = FastEmbedEmbeddings()

#LLM model
ollama_url = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
llm = OllamaLLM(model="llama3", base_url=ollama_url)

#input for AI behavior
raw_prompt = PromptTemplate.from_template("""
<s>[INST] You are a technical assistant good at searching documents. 
If you do not have an answer from provided information say so. [/INST]</s> 
[INST] {input}
Context:{context}
Answer:
[/INST]
""")

def answer_query(request):


    json_content = request.get_json()


    if not json_content or "query" not in json_content:
        return jsonify({"error": "Missing 'query' in request body"}), 400
    

    query = json_content.get("query")


    vector_store = Chroma(persist_directory=folder_path, embedding_function=embedding)
    retriever = vector_store.as_retriever(search_type="similarity_score_threshold", search_kwargs={"k": 5, "score_threshold": 0.3})

    #RAG chain
    document_chain = create_stuff_documents_chain(llm, raw_prompt)
    chain = create_retrieval_chain(retriever, document_chain)

    result = chain.invoke({"input": query})
    return jsonify({"answer": result.get("answer", "").strip()})
