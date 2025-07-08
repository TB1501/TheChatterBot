import os
import shutil
from flask import jsonify
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_chroma import Chroma

#Initialize a text splitter that breaks large documents into smaller chunks
text_spliter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=80, length_function=len, is_separator_regex=False)

#Create an embedding model using FastEmbed, which will convert text into vector representations
embedding = FastEmbedEmbeddings()

#Path to the folder where processed document data is stored
folder_path = "db"

def process_pdf(request):
    #Check if the file was included in the request
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    #Retrieving the uploaded file    
    file = request.files["file"]

    #Clear old data
    for path in ["docs", folder_path]:
        if os.path.exists(path):
            shutil.rmtree(path)

    #Create a new docs directory for storing new data
    os.makedirs("docs", exist_ok=True)

    #Save upload file
    file_path = os.path.join("docs", file.filename)
    file.save(file_path)

    #Load and split the file in seperate pages
    loader = PyMuPDFLoader(file_path)
    documents = loader.load_and_split()
    chunks = text_spliter.split_documents(documents)

    #Create a storage vector to store the chunks using embeddings
    Chroma.from_documents(documents=chunks, embedding=embedding, persist_directory=folder_path)

    return jsonify({
        "Status": "Successfully uploaded",
        "filename": file.filename,
        "pages": len(documents),
        "chunks": len(chunks)
    })
