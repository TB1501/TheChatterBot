The ChatterBot is an AI powered chatbot that helps you analyze your PDF documents. The ChatterBots AI is based on the Ollama framework.

## Components

This project integrates the following components:

- **Flask**: For the web interface and routing.
- **LangChain**: Powers the document chains and retrieval logic.
- **Chroma**: Vector store for document chunk embeddings.
- **FastEmbedEmbeddings**: To embed document content efficiently.
- **Ollama + LLaMA3**: Local language model for response generation.

## Setup and Deployment

**Requirments**:
1. Python 3.10+
2. Pip
3. Ollama [Ollama's official website](https://ollama.com/download) downloaded and installed for your OS

**Install dependencies**:

1. Run the llama3 model in CMD:
    ```sh
    ollama pull llama3
    ```
2. Clone the repository and navigate to the project folder:
    ```sh
    https://github.com/TB1501/TheChatterBot.git
    ```
3. Create a virtual environment:
    ```sh
    python -m venv venv
    venv\Scripts\activate
    ```
4. Install the required libraries:
    ```sh
    pip install -r requirements.txt
    ```
5. Run the application:
    ```sh
    py app.py
    ```
6. Navigate to `http://localhost:8080/`**

7. Register

8. Login

9. Chat with bot

## 🤖 Happy Chating!