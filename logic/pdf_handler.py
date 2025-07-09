import os
import shutil
from flask import jsonify
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_chroma import Chroma


text_spliter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=80, length_function=len, is_separator_regex=False)

#embedding model
embedding = FastEmbedEmbeddings()

#db for processed data
folder_path = "db"

def process_pdf(request):

    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
   
    file = request.files["file"]

    for path in ["docs", folder_path]:
        if os.path.exists(path):
            shutil.rmtree(path)


    os.makedirs("docs", exist_ok=True)

    file_path = os.path.join("docs", file.filename)
    file.save(file_path)


    loader = PyMuPDFLoader(file_path)
    documents = loader.load_and_split()
    chunks = text_spliter.split_documents(documents)

    Chroma.from_documents(documents=chunks, embedding=embedding, persist_directory=folder_path)

    return jsonify({
        "Status": "Successfully uploaded",
        "filename": file.filename,
        "pages": len(documents),
        "chunks": len(chunks)
    })
