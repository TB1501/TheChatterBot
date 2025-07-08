from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
import os
from langchain_ollama import OllamaLLM
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_chroma import Chroma
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.prompts import PromptTemplate
import shutil



# Import the Flask web framework
app = Flask(__name__)
app.secret_key = 'test_secret_key'

# Path to the folder where processed document data is stored
folder_path="db"

#Simulated db for Users
users={}

# Initialize a cached instance of the LLM using the llama3 model
cahched_llm=OllamaLLM(model="llama3")

# Create an embedding model using FastEmbed, which will convert text into vector representations
embedding = FastEmbedEmbeddings()

# Initialize a text splitter that breaks large documents into smaller chunks
text_spliter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=80, length_function=len, is_separator_regex=False)

# Define a raw prompt template that will be used to format input for the LLM
# The prompt guides the model to behave like a technical assistant
# It instructs the LLM to respond only if the answer is found in the given context
raw_prompt=PromptTemplate.from_template(""" <s>[INST] You are a technical assistant good ad searching documents. 
                                        If you do not have an answer from provided information say so. [/INST]</s> 
                                        [INST] {input}
                                            Context:{context}
                                            Answer:
                                        [/INST]
                                        """)

#Home page
@app.route('/')
def home():
    return render_template('home.html')

#Handling the registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash("Username already exists. Please log in.", "error")
            return redirect(url_for('login'))
        users[username] = password
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

#Handling the login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user is registered and password matches
        if username in users and users[username] == password:
            session['user'] = username
            return redirect(url_for('chat'))
        else:
            flash("Invalid credentials or unregistered user.", "error")
    return render_template('login.html')

#Handling the logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

#ChatterBot
@app.route('/chat')
def chat():
    return render_template('chat.html')


#Handling questions about the document
@app.route("/ask", methods=["POST"])
def askPost():
    print("[INFO] POST /ask called")

    # Parse JSON from request
    json_content=request.get_json()
    if not json_content or "query" not in json_content:
        print("[ERROR] Missing 'query' in request body")
        return jsonify({"error": "Missing 'query' in request body"}), 400
    
    query = json_content.get("query")
    print(f"[INFO] Received query: {query}")

    # Load the vector store from disk
    print("[INFO] Loading vector store")
    vector_store=Chroma(persist_directory=folder_path, embedding_function=embedding)

    
    # Create a retriever from the vector store
    print("[INFO] Creating retriever")
    retriever=vector_store.as_retriever(search_type="similarity_score_threshold", search_kwargs={"k":5, "score_threshold":0.3})

    # RAG chain
    print("[INFO] Building document chain")
    document_chain=create_stuff_documents_chain(cahched_llm, raw_prompt)
    chain=create_retrieval_chain(retriever, document_chain)

    # Run the chain with the user's query
    print("[INFO] Running the chain")
    result = chain.invoke({"input":query})
    print("[INFO] Answer generated")

    response_answer = {"answer": result["answer"]}

    return jsonify(response_answer)


#Handle PDF upload
@app.route("/pdf", methods=["POST"])
def pdfPost():
    print("[INFO] POST /pdf called")

    # Check if the file was included in the request
    if "file" not in request.files:
        print("[ERROR] No file in the request")
        return jsonify({"error": "No file provided"}), 400
    
    #Retrieving the uploaded file
    file = request.files["file"]

    # Clean previous files
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

    # Create a new docs directory for storing the new upload
    os.makedirs("docs", exist_ok=True)

    # Save new file
    file_name = file.filename
    save_file = os.path.join("docs", file_name)
    file.save(save_file)
    print(f"[INFO] Saved file: {file_name}")

    #Load and split the file in seperate pages
    loader = PyMuPDFLoader(save_file)
    documents = loader.load_and_split()
    print(f"[INFO] PDF loaded with {len(documents)} pages")

    # Split the pages into chunks for embedding
    chunks =text_spliter.split_documents(documents)
    print(f"[INFO] Document split into {len(chunks)} chunks")

     # Create a storage vector to store the chunks using embeddings
    vector_store=Chroma.from_documents(documents=chunks, embedding=embedding, persist_directory=folder_path)
    #vector_store.persist()
    print("[INFO] Vector store created and saved")

    #Result
    response = {"Status":"Successfully uploaded", "filename":file_name, "pages":len(documents), "chunks":len(chunks)}
    return jsonify(response)

def start_app():
    app.run(host="0.0.0.0", port=8080, debug=True)

if __name__ == "__main__":
    start_app()